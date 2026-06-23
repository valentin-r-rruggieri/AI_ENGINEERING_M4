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

from github_mcp_utils import (
    AUDIT_LOG_PATH,
    create_repo,
    get_repo,
    read_recent_audit_events,
    upsert_file,
)


# 1) El MCP server lee el `.env` del bloque de ejercicios. Asi Antigravity,
# VS Code o el host Python pueden pasar GITHUB_TOKEN sin hardcodearlo.
EXERCISES_DIR = Path(__file__).resolve().parents[1]
load_dotenv(EXERCISES_DIR / ".env")


# 2) Modelos de salida: cada tool/resource devuelve contratos claros, no texto
# suelto. Esto ayuda al Host y al LLM a seguir trabajando con datos tipados.
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


class GitHubCapabilities(BaseModel):
    """Resource docente: cataloga capacidades y riesgos del server."""

    tools: list[dict[str, Any]]
    resources: list[dict[str, Any]]
    prompts: list[dict[str, Any]]
    teaching_rule: str


class GitHubSecurityPolicy(BaseModel):
    """Resource docente: resume reglas operativas del MCP."""

    default_private_repos: bool
    destructive_tools_enabled: bool
    token_exposed_in_resources: bool
    audit_enabled: bool
    recommended_token_scope: str
    rules: list[str]


class GitHubAuditRecent(BaseModel):
    """Resource docente: ultimos eventos de auditoria sin secretos."""

    audit_log_path: str
    event_count: int
    events: list[dict[str, Any]]


class GitHubReadmeTemplate(BaseModel):
    """Resource docente: template reusable para README.md."""

    name: str
    path: str
    template: str


def build_mcp() -> Any:
    """Construye el server dentro de una funcion para que pueda importarse en tests."""
    from mcp.server.fastmcp import FastMCP

    # 3) FastMCP crea el servidor y luego los decoradores publican capacidades.
    # Lo que este objeto registra es lo que Antigravity descubre por protocolo.
    mcp = FastMCP("AEM4L3 GitHub MCP")

    # 4) Tools: acciones invocables. Estas pueden tener side effects reales,
    # por eso el contrato es explicito y el repo se crea privado por defecto.
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

    # 5) Resources: contexto de lectura. Sirven para informar al Host sin
    # ejecutar acciones ni exponer secretos como GITHUB_TOKEN.
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

    @mcp.resource("github://capabilities")
    def github_capabilities() -> GitHubCapabilities:
        """Expone el catalogo completo: tools, resources y prompts."""
        return GitHubCapabilities(
            tools=[
                {
                    "name": "github_create_repo",
                    "kind": "tool",
                    "side_effect": True,
                    "risk": "high",
                    "purpose": "Crear repositorios privados en GitHub.",
                },
                {
                    "name": "github_upsert_file",
                    "kind": "tool",
                    "side_effect": True,
                    "risk": "high",
                    "purpose": "Crear o actualizar archivos con commits reales.",
                },
                {
                    "name": "github_get_repo",
                    "kind": "tool",
                    "side_effect": False,
                    "risk": "low",
                    "purpose": "Consultar metadata de repositorios.",
                },
            ],
            resources=[
                {
                    "uri": "github://config",
                    "purpose": "Mostrar configuracion segura del server.",
                },
                {
                    "uri": "github://capabilities",
                    "purpose": "Explicar las capacidades disponibles y su riesgo.",
                },
                {
                    "uri": "github://security-policy",
                    "purpose": "Describir reglas de seguridad y operacion.",
                },
                {
                    "uri": "github://audit/recent",
                    "purpose": "Mostrar eventos recientes sin secretos.",
                },
                {
                    "uri": "github://templates/readme-basic",
                    "purpose": "Proveer un template base para README.md.",
                },
            ],
            prompts=[
                {
                    "name": "repo_bootstrap_prompt",
                    "purpose": "Guiar la creacion inicial de un repo privado.",
                },
                {
                    "name": "repo_readme_prompt",
                    "purpose": "Generar un README claro para una audiencia.",
                },
                {
                    "name": "safe_github_action_prompt",
                    "purpose": "Revisar riesgos antes de usar tools con side effects.",
                },
                {
                    "name": "repo_review_prompt",
                    "purpose": "Guiar una revision conceptual de un repositorio.",
                },
            ],
            teaching_rule="Tool ejecuta; resource informa; prompt guia.",
        )

    @mcp.resource("github://security-policy")
    def github_security_policy() -> GitHubSecurityPolicy:
        """Expone politicas de seguridad sin filtrar secretos."""
        return GitHubSecurityPolicy(
            default_private_repos=True,
            destructive_tools_enabled=False,
            token_exposed_in_resources=False,
            audit_enabled=True,
            recommended_token_scope="Permisos minimos para crear repos y escribir contenido.",
            rules=[
                "Los repos se crean privados por defecto.",
                "No existe tool de borrado.",
                "GITHUB_TOKEN nunca se devuelve en resources ni errores docentes.",
                "Las tools con side effects deben quedar auditadas.",
                "El audit log guarda metadata operativa, no secretos.",
            ],
        )

    @mcp.resource("github://audit/recent")
    def github_audit_recent() -> GitHubAuditRecent:
        """Devuelve eventos recientes para mostrar trazabilidad en clase."""
        events = read_recent_audit_events(limit=10)
        return GitHubAuditRecent(
            audit_log_path=str(AUDIT_LOG_PATH),
            event_count=len(events),
            events=events,
        )

    @mcp.resource("github://templates/readme-basic")
    def github_readme_basic_template() -> GitHubReadmeTemplate:
        """Template de README que un host puede usar antes de llamar upsert_file."""
        return GitHubReadmeTemplate(
            name="readme-basic",
            path="README.md",
            template=(
                "# {project_name}\n\n"
                "{goal}\n\n"
                "## Objetivo\n\n"
                "Explicar para que existe este repositorio.\n\n"
                "## Estructura inicial\n\n"
                "- `README.md`: descripcion del proyecto.\n\n"
                "## Proximos pasos\n\n"
                "1. Definir alcance.\n"
                "2. Agregar archivos iniciales.\n"
                "3. Documentar decisiones tecnicas.\n"
            ),
        )

    # 6) Prompts: plantillas reutilizables. No ejecutan GitHub; guian al LLM
    # para decidir, redactar o revisar antes de llamar tools.
    @mcp.prompt()
    def repo_bootstrap_prompt(project_name: str, goal: str) -> str:
        """Prompt reutilizable para pedirle a un LLM que inicialice un repo."""
        return (
            "Actua como un asistente de ingenieria. "
            f"Tenemos que crear el repositorio `{project_name}` para este objetivo: {goal}. "
            "Primero crea un repo privado. Despues agrega un README.md claro con objetivo, "
            "estructura inicial y proximos pasos."
        )

    @mcp.prompt()
    def repo_readme_prompt(project_name: str, goal: str, audience: str = "desarrolladores") -> str:
        """Prompt para generar un README antes de llamar `github_upsert_file`."""
        return (
            "Genera el contenido completo de un README.md en Markdown. "
            f"Proyecto: `{project_name}`. Objetivo: {goal}. Audiencia: {audience}. "
            "Inclui secciones de objetivo, estructura inicial, como probarlo y proximos pasos. "
            "No inventes credenciales, tokens ni URLs privadas."
        )

    @mcp.prompt()
    def safe_github_action_prompt(action_summary: str) -> str:
        """Prompt para revisar riesgos antes de ejecutar side effects en GitHub."""
        return (
            "Antes de ejecutar una accion real en GitHub, revisa el riesgo operativo. "
            f"Accion solicitada: {action_summary}. "
            "Responde con: 1) tool MCP sugerida, 2) side effects, 3) permisos necesarios, "
            "4) datos que no deben exponerse, 5) confirmacion recomendada antes de ejecutar."
        )

    @mcp.prompt()
    def repo_review_prompt(owner: str, repo: str) -> str:
        """Prompt para guiar una revision conceptual de metadata del repo."""
        return (
            "Actua como revisor tecnico. Usa primero `github_get_repo` para consultar metadata. "
            f"Repositorio: `{owner}/{repo}`. "
            "Luego resume visibilidad, branch por defecto, freshness del repo y posibles riesgos. "
            "No intentes borrar ni modificar archivos durante esta revision."
        )

    return mcp


try:
    # 7) Construimos el server a nivel modulo para que `mcp.run()` pueda usarlo
    # cuando el archivo se ejecuta como proceso STDIO.
    mcp = build_mcp()
except ModuleNotFoundError as exc:
    if exc.name != "mcp":
        raise
    mcp = None


def main() -> None:
    """Ejecucion directa por STDIO, compatible con clientes MCP locales."""
    if mcp is None:
        raise RuntimeError('Falta instalar la dependencia MCP: pip install "mcp[cli]>=1.27,<2"')
    # 8) En STDIO el proceso queda esperando mensajes MCP del cliente.
    # No es una API HTTP: Antigravity habla con este proceso por stdin/stdout.
    mcp.run()


if __name__ == "__main__":
    main()
