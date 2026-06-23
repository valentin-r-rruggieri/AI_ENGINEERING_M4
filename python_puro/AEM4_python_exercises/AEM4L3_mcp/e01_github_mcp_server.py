# pyright: reportMissingImports=false
"""
E01 - MCP server real para GitHub por STDIO
AEM4L3 | Model Context Protocol

Objetivo pedagogico:
    Construir un MCP Server minimo, real y usable desde Antigravity.
    El server expone GitHub como capacidades gobernadas: tools, resource y prompt.

Como correrlo como MCP server:
    python python_puro/AEM4_python_exercises/AEM4L3_mcp/e01_github_mcp_server.py

Variables requeridas:
    GITHUB_TOKEN: token real de GitHub con permisos para crear repos y escribir contenido.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from github_mcp_utils import AUDIT_LOG_PATH, create_repo, get_repo, upsert_file


EXERCISES_DIR = Path(__file__).resolve().parents[1]
load_dotenv(EXERCISES_DIR / ".env")


class GitHubRepoResult(BaseModel):
    """Salida estructurada de `github_create_repo`.

    El MCP SDK puede exponer este tipo como structured output. Para clase,
    sirve para mostrar que una tool no devuelve texto suelto sino contrato.
    """

    id: int
    name: str
    full_name: str
    owner: str
    private: bool
    default_branch: str
    html_url: str


class GitHubFileResult(BaseModel):
    """Salida estructurada de `github_upsert_file`."""

    repo: str
    path: str
    branch: str
    created_or_updated: str
    commit_sha: str
    commit_url: str
    content_url: str


class GitHubConfig(BaseModel):
    """Resource seguro: muestra estado operacional sin exponer secretos."""

    server_name: str
    transport: str
    token_configured: bool
    default_private_repos: bool
    audit_log_path: str
    dangerous_tools_exposed: list[str]


def build_mcp() -> Any:
    """Construye el server dentro de una funcion para que pueda importarse en tests."""
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("AEM4L3 GitHub MCP")

    @mcp.tool()
    def github_create_repo(
        name: Annotated[str, Field(min_length=3, description="Nombre del repositorio a crear.")],
        description: Annotated[str, Field(description="Descripcion corta del repositorio.")] = "",
        private: Annotated[bool, Field(description="Crear repo privado por defecto.")] = True,
    ) -> GitHubRepoResult:
        """Crea un repositorio privado en GitHub.

        Esta tool tiene side effects reales. Por eso el repo se crea privado por
        defecto y no existe ninguna tool de borrado en este ejercicio.
        """
        return GitHubRepoResult(**create_repo(name=name, description=description, private=private))

    @mcp.tool()
    def github_upsert_file(
        owner: Annotated[str, Field(description="Owner u organizacion del repo.")],
        repo: Annotated[str, Field(description="Nombre del repo.")],
        path: Annotated[str, Field(description="Ruta del archivo dentro del repo.")],
        content: Annotated[str, Field(description="Contenido completo del archivo.")],
        commit_message: Annotated[str, Field(min_length=5, description="Mensaje del commit.")],
        branch: Annotated[str, Field(description="Branch destino.")] = "main",
    ) -> GitHubFileResult:
        """Crea o actualiza un archivo y genera un commit real."""
        return GitHubFileResult(
            **upsert_file(
                owner=owner,
                repo=repo,
                path=path,
                content=content,
                commit_message=commit_message,
                branch=branch,
            )
        )

    @mcp.tool()
    def github_get_repo(
        owner: Annotated[str, Field(description="Owner u organizacion del repo.")],
        repo: Annotated[str, Field(description="Nombre del repo.")],
    ) -> dict[str, Any]:
        """Consulta metadata de un repositorio existente."""
        return get_repo(owner=owner, repo=repo)

    @mcp.resource("github://config")
    def github_config() -> GitHubConfig:
        """Expone configuracion segura del server sin revelar GITHUB_TOKEN."""
        return GitHubConfig(
            server_name="AEM4L3 GitHub MCP",
            transport="stdio",
            token_configured=bool(os.getenv("GITHUB_TOKEN")),
            default_private_repos=True,
            audit_log_path=str(AUDIT_LOG_PATH),
            dangerous_tools_exposed=[],
        )

    @mcp.prompt()
    def repo_bootstrap_prompt(project_name: str, goal: str) -> str:
        """Prompt reutilizable para pedirle a un LLM que inicialice un repo."""
        return (
            "Actua como un asistente de ingenieria. "
            f"Tenemos que crear el repositorio `{project_name}` para este objetivo: {goal}. "
            "Primero crea un repo privado. Despues agrega un README.md claro con objetivo, "
            "estructura inicial y proximos pasos."
        )

    return mcp


try:
    mcp = build_mcp()
except ModuleNotFoundError as exc:
    if exc.name != "mcp":
        raise
    mcp = None


def main() -> None:
    """Ejecucion directa por STDIO, compatible con clientes MCP locales."""
    if mcp is None:
        raise RuntimeError('Falta instalar la dependencia MCP: pip install "mcp[cli]>=1.27,<2"')
    mcp.run()


if __name__ == "__main__":
    main()
