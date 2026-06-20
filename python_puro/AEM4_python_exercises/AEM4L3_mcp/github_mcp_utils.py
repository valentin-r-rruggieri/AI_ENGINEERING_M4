"""Utilidades para el MCP real de GitHub de AEM4L3.

Estas funciones separan la logica de GitHub del servidor MCP para que la clase
pueda explicar dos capas distintas:

- MCP expone tools, resources y prompts.
- Esta utilidad ejecuta llamadas HTTP reales contra GitHub.

No se usa PyGithub a proposito: con `httpx` el alumno ve claramente que el MCP
server termina gobernando una API externa comun.
"""

from __future__ import annotations

import base64
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx


GITHUB_API_URL = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"
DATA_DIR = Path(__file__).parent / "data"
AUDIT_LOG_PATH = DATA_DIR / "github_mcp_audit_log.jsonl"


def get_github_token() -> str:
    """Lee el token real de GitHub y falla antes de tocar la API si falta."""
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "Falta GITHUB_TOKEN. Agregalo al .env para ejecutar el MCP real de GitHub."
        )
    return token


def github_headers(token: str) -> dict[str, str]:
    """Centraliza headers para no repetirlos en cada tool."""
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }


def github_request(
    method: str,
    path: str,
    *,
    token: str,
    payload: dict[str, Any] | None = None,
    ok_statuses: tuple[int, ...] = (200, 201),
) -> dict[str, Any]:
    """Ejecuta una llamada REST a GitHub y devuelve JSON validado.

    El error evita imprimir secretos. GitHub nunca recibe logs con el token.
    """
    response = httpx.request(
        method,
        f"{GITHUB_API_URL}{path}",
        headers=github_headers(token),
        json=payload,
        timeout=30,
    )
    if response.status_code not in ok_statuses:
        detail: Any
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(
            f"GitHub API error {response.status_code} en {method} {path}: {detail}"
        )
    if not response.content:
        return {}
    return response.json()


def append_audit_event(tool_name: str, payload: dict[str, Any]) -> None:
    """Registra auditoria local sin token ni contenido sensible.

    La auditoria muestra governance: quien ejecuto, que tool, contra que repo y
    cuando. Para clase es suficiente y evita guardar secretos por accidente.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    safe_payload = {
        "timestamp": datetime.now(UTC).isoformat(),
        "tool": tool_name,
        **payload,
    }
    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(safe_payload, ensure_ascii=False) + "\n")


def create_repo(name: str, description: str, private: bool = True) -> dict[str, Any]:
    """Crea un repo real en GitHub y lo inicializa con branch main."""
    token = get_github_token()
    result = github_request(
        "POST",
        "/user/repos",
        token=token,
        payload={
            "name": name,
            "description": description,
            "private": private,
            "auto_init": True,
        },
    )
    append_audit_event(
        "github_create_repo",
        {
            "repo": result.get("full_name"),
            "private": private,
            "html_url": result.get("html_url"),
        },
    )
    return {
        "id": result["id"],
        "name": result["name"],
        "full_name": result["full_name"],
        "owner": result["owner"]["login"],
        "private": result["private"],
        "default_branch": result["default_branch"],
        "html_url": result["html_url"],
    }


def get_repo(owner: str, repo: str) -> dict[str, Any]:
    """Lee metadata de un repo para que el cliente pueda verificar estado."""
    token = get_github_token()
    result = github_request("GET", f"/repos/{owner}/{repo}", token=token)
    append_audit_event(
        "github_get_repo",
        {"repo": result.get("full_name"), "private": result.get("private")},
    )
    return {
        "name": result["name"],
        "full_name": result["full_name"],
        "private": result["private"],
        "default_branch": result["default_branch"],
        "html_url": result["html_url"],
        "updated_at": result["updated_at"],
    }


def get_existing_file_sha(owner: str, repo: str, path: str, branch: str, token: str) -> str | None:
    """Devuelve el SHA actual si el archivo existe; `None` si hay que crearlo."""
    response = httpx.get(
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}",
        headers=github_headers(token),
        params={"ref": branch},
        timeout=30,
    )
    if response.status_code == 404:
        return None
    if response.status_code != 200:
        raise RuntimeError(
            f"GitHub API error {response.status_code} buscando {path}: {response.text}"
        )
    return response.json().get("sha")


def upsert_file(
    owner: str,
    repo: str,
    path: str,
    content: str,
    commit_message: str,
    branch: str = "main",
) -> dict[str, Any]:
    """Crea o actualiza un archivo en GitHub con un commit real."""
    token = get_github_token()
    sha = get_existing_file_sha(owner, repo, path, branch, token)
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("ascii")
    payload: dict[str, Any] = {
        "message": commit_message,
        "content": encoded_content,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    result = github_request(
        "PUT",
        f"/repos/{owner}/{repo}/contents/{path}",
        token=token,
        payload=payload,
    )
    append_audit_event(
        "github_upsert_file",
        {
            "repo": f"{owner}/{repo}",
            "path": path,
            "branch": branch,
            "content_chars": len(content),
            "commit_sha": result["commit"]["sha"],
        },
    )
    return {
        "repo": f"{owner}/{repo}",
        "path": path,
        "branch": branch,
        "created_or_updated": "updated" if sha else "created",
        "commit_sha": result["commit"]["sha"],
        "commit_url": result["commit"]["html_url"],
        "content_url": result["content"]["html_url"],
    }
