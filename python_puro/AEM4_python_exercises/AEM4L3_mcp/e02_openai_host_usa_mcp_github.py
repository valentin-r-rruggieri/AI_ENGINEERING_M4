# pyright: reportMissingImports=false
"""
E02 - Host OpenAI usando el MCP de GitHub por STDIO
AEM4L3 | Model Context Protocol

Objetivo pedagogico:
    Mostrar la diferencia entre MCP Host, MCP Client y MCP Server.
    Este script funciona como host: usa OpenAI para planificar la accion,
    levanta el server MCP por STDIO y ejecuta tools reales de GitHub.

Importante:
    Ejecutarlo crea un repo privado real si hay GITHUB_TOKEN valido.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Literal, cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import require_openai_api_key, trace_json, trace_text
from AEM4L3_mcp.github_mcp_utils import get_authenticated_login


load_dotenv(ROOT_DIR / ".env")
require_openai_api_key()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SERVER_PATH = Path(__file__).with_name("e01_github_mcp_server.py")


class CreateRepoArgs(BaseModel):
    """Argumentos que el LLM debe producir para la primera tool MCP."""

    name: str = Field(..., min_length=3)
    description: str
    private: bool = True


class MCPToolDecision(BaseModel):
    """Plan minimo: el LLM elige una tool disponible y sus argumentos."""

    tool_name: Literal["github_create_repo"]
    args: CreateRepoArgs
    reasoning: str


def require_github_token() -> None:
    """Falla temprano para no abrir una sesion MCP que luego no puede ejecutar."""
    if not os.getenv("GITHUB_TOKEN"):
        raise RuntimeError("Falta GITHUB_TOKEN. Este ejercicio usa GitHub real.")


def serialize_mcp_result(result: Any) -> Any:
    """Convierte resultados MCP/Pydantic a JSON imprimible."""
    if hasattr(result, "model_dump"):
        return result.model_dump(mode="json")
    if hasattr(result, "__dict__"):
        return result.__dict__
    return str(result)


def extract_structured_content(result: Any) -> dict[str, Any]:
    """Obtiene structured output aunque cambie el casing entre versiones SDK."""
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict):
        return structured
    dumped = serialize_mcp_result(result)
    if isinstance(dumped, dict):
        maybe_structured = dumped.get("structuredContent") or dumped.get("structured_content")
        if isinstance(maybe_structured, dict):
            return maybe_structured
    raise RuntimeError("El MCP result no incluyo structured output para continuar el flujo.")


def choose_repo_tool(user_request: str, available_tools: list[dict[str, Any]]) -> MCPToolDecision:
    """Pide a OpenAI que elija la tool MCP inicial.

    La lista de tools viene del server MCP, no de una lista hardcodeada en el
    prompt. Esa es la idea central: el host descubre capacidades.
    """
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Sos un MCP Host. Elegi una tool disponible para cumplir el pedido. "
                "Para este ejercicio solo podes iniciar creando un repo privado.",
            ),
            (
                "user",
                "Pedido del usuario:\n{user_request}\n\nTools disponibles:\n{tools}",
            ),
        ]
    )
    structured_llm = ChatOpenAI(model=MODEL_NAME, temperature=0).with_structured_output(MCPToolDecision)
    chain = prompt | structured_llm
    return cast(MCPToolDecision, chain.invoke({"user_request": user_request, "tools": available_tools}))


async def run_host(user_request: str) -> None:
    """Levanta el server por STDIO, lista tools y ejecuta el flujo completo."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    require_github_token()

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        env=dict(os.environ),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            available_tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema,
                }
                for tool in tools_result.tools
            ]

            decision = choose_repo_tool(user_request, available_tools)
            github_owner = get_authenticated_login()
            existing_repo = await session.call_tool(
                "github_get_repo",
                arguments={"owner": github_owner, "repo": decision.args.name},
            )

            if existing_repo.isError:
                create_result = await session.call_tool(
                    decision.tool_name,
                    arguments=decision.args.model_dump(mode="json"),
                )
                if create_result.isError:
                    raise RuntimeError(serialize_mcp_result(create_result))
                create_payload = serialize_mcp_result(create_result)
                structured = extract_structured_content(create_result)
                repo_owner = structured["owner"]
                repo_name = structured["name"]
                default_branch = structured.get("default_branch", "main")
            else:
                existing_payload = extract_structured_content(existing_repo)
                create_payload = {
                    "reused_existing_repo": True,
                    "repo": existing_payload,
                }
                repo_owner = github_owner
                repo_name = decision.args.name
                default_branch = existing_payload.get("default_branch", "main")

            # El segundo paso usa el owner/repo real devuelto por GitHub. Lo hace
            # el host porque depende del resultado de la primera tool.
            readme = (
                f"# {repo_name}\n\n"
                f"{decision.args.description}\n\n"
                "## Objetivo\n\n"
                "Repositorio creado desde un MCP server propio para AEM4L3.\n\n"
                "## Flujo demostrado\n\n"
                "1. OpenAI decide la accion inicial.\n"
                "2. El MCP Host llama al MCP Server por STDIO.\n"
                "3. El MCP Server ejecuta GitHub con un contrato gobernado.\n"
            )
            file_result = await session.call_tool(
                "github_upsert_file",
                arguments={
                    "owner": repo_owner,
                    "repo": repo_name,
                    "path": "README.md",
                    "content": readme,
                    "commit_message": "Add initial README from custom MCP",
                    "branch": default_branch,
                },
            )

            trace_text("USER", user_request)
            trace_json("MCP_TOOLS", available_tools)
            trace_json("LLM_TOOL_CALL", decision.model_dump(mode="json"))
            trace_json("MCP_RESULT", {"create_repo": create_payload, "upsert_file": serialize_mcp_result(file_result)})


def main() -> None:
    user_request = (
        "Crea un repo privado llamado aem4l3-mcp-demo con un README inicial "
        "para mostrar en clase como Antigravity podria usar nuestro MCP."
    )
    asyncio.run(run_host(user_request))


if __name__ == "__main__":
    main()
