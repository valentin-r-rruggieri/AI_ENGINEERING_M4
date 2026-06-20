# pyright: reportMissingImports=false
"""
E06 - MCP integrador: soporte educativo con tools, resources, prompts y governance
AEM4L3 | Model Context Protocol

Objetivo pedagogico:
    Unir toda la lecture en un ejemplo compacto: server, tools, resources,
    prompts, schemas, scopes, tenant isolation, auditoria y versionado.

Este ejercicio no llama APIs externas. Simula side effects con contratos reales
para que el foco sea arquitectura MCP y no credenciales.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any, Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator


EXERCISES_DIR = Path(__file__).resolve().parents[1]
load_dotenv(EXERCISES_DIR / ".env")

DATA_DIR = Path(__file__).parent / "data"
AUDIT_LOG_PATH = DATA_DIR / "support_mcp_audit_log.jsonl"


class AuthContext(BaseModel):
    """Contexto confiable derivado del token, no de parametros del cliente."""

    tenant_id: str
    actor_id: str
    scopes: list[str]


class TicketV1(BaseModel):
    """Schema legacy: suficiente para crear un ticket simple."""

    customer_id: str
    issue: str = Field(..., min_length=10)


class TicketV2(BaseModel):
    """Schema nuevo: agrega campos operativos y versiona el contrato."""

    customer_id: str
    issue: str = Field(..., min_length=10)
    priority: Literal["low", "medium", "high"]
    source: Literal["chat", "email", "phone"] = "chat"


class ToolAuditEvent(BaseModel):
    """Evento de auditoria sin datos sensibles."""

    timestamp: str
    tenant_id: str
    actor_id: str
    tool: str
    allowed: bool
    reason: str


class TicketResult(BaseModel):
    """Salida estructurada de la tool `create_support_ticket_v2`."""

    ticket_id: str
    tenant_id: str
    customer_id: str
    priority: str
    status: str
    schema_version: str


def load_auth_context() -> AuthContext:
    """Carga un contexto de autorizacion simple para clase.

    En produccion esto vendria de OAuth/JWT. Aca usamos variables de entorno
    para mostrar que el tenant y los scopes no deben venir del body de la tool.
    """
    return AuthContext(
        tenant_id=os.getenv("MCP_TENANT_ID", "tenant_demo"),
        actor_id=os.getenv("MCP_ACTOR_ID", "instructor"),
        scopes=os.getenv("MCP_SCOPES", "tickets:read,tickets:write,policies:read").split(","),
    )


def append_audit(event: ToolAuditEvent) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event.model_dump(mode="json"), ensure_ascii=False) + "\n")


def authorize(required_scope: str, ctx: AuthContext, tool_name: str) -> None:
    """Gate de scopes: el LLM puede pedir, pero el server decide."""
    allowed = required_scope in ctx.scopes
    event = ToolAuditEvent(
        timestamp=datetime.now(UTC).isoformat(),
        tenant_id=ctx.tenant_id,
        actor_id=ctx.actor_id,
        tool=tool_name,
        allowed=allowed,
        reason="scope_ok" if allowed else f"missing_scope:{required_scope}",
    )
    append_audit(event)
    if not allowed:
        raise PermissionError(event.reason)


def migrate_ticket_v1_to_v2(payload: TicketV1) -> TicketV2:
    """Adaptador de compatibilidad para clientes viejos."""
    return TicketV2(customer_id=payload.customer_id, issue=payload.issue, priority="medium", source="chat")


def build_mcp() -> Any:
    """Construye el server para que pueda ejecutarse por STDIO."""
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("AEM4L3 Support Governance MCP")

    @mcp.resource("support://refund-policy")
    def refund_policy() -> str:
        """Resource: contexto de lectura que no deberia tener side effects."""
        return (
            "Politica de reembolso demo: pedidos demorados mas de 72 horas pueden "
            "abrir ticket de revision. No prometer reembolso automatico sin validar orden."
        )

    @mcp.prompt()
    def support_triage_prompt(customer_message: str) -> str:
        """Prompt reutilizable para normalizar triage de soporte."""
        return (
            "Clasifica el mensaje del cliente, identifica riesgo y propone una accion. "
            f"Mensaje: {customer_message}"
        )

    @mcp.tool()
    def create_support_ticket_v2(
        customer_id: Annotated[str, Field(description="ID del cliente dentro del tenant activo.")],
        issue: Annotated[str, Field(min_length=10, description="Problema reportado por el cliente.")],
        priority: Annotated[Literal["low", "medium", "high"], Field(description="Prioridad operativa.")],
        source: Annotated[Literal["chat", "email", "phone"], Field(description="Canal de origen.")] = "chat",
    ) -> TicketResult:
        """Tool con side effect simulado, protegida por scope `tickets:write`."""
        ctx = load_auth_context()
        authorize("tickets:write", ctx, "create_support_ticket_v2")
        ticket = TicketV2(customer_id=customer_id, issue=issue, priority=priority, source=source)
        return TicketResult(
            ticket_id=f"TCK-{datetime.now(UTC).strftime('%H%M%S')}",
            tenant_id=ctx.tenant_id,
            customer_id=ticket.customer_id,
            priority=ticket.priority,
            status="created",
            schema_version="2.0.0",
        )

    @mcp.tool()
    def create_support_ticket_v1(customer_id: str, issue: str) -> TicketResult:
        """Tool legacy que migra a v2 para no romper clientes existentes."""
        legacy = TicketV1(customer_id=customer_id, issue=issue)
        migrated = migrate_ticket_v1_to_v2(legacy)
        ctx = load_auth_context()
        authorize("tickets:write", ctx, "create_support_ticket_v1")
        return TicketResult(
            ticket_id=f"TCK-{datetime.now(UTC).strftime('%H%M%S')}",
            tenant_id=ctx.tenant_id,
            customer_id=migrated.customer_id,
            priority=migrated.priority,
            status="created",
            schema_version="1.0.0->2.0.0",
        )

    @mcp.tool()
    def unsafe_confused_deputy_example(tenant_id_from_client: str, customer_id: str) -> dict[str, Any]:
        """Ejemplo didactico: muestra por que no confiar en tenant del cliente."""
        ctx = load_auth_context()
        return {
            "risk": "confused_deputy",
            "client_claimed_tenant": tenant_id_from_client,
            "trusted_tenant_from_context": ctx.tenant_id,
            "decision": "reject_client_tenant_parameter",
            "customer_id": customer_id,
        }

    return mcp


try:
    mcp = build_mcp()
except ModuleNotFoundError as exc:
    if exc.name != "mcp":
        raise
    mcp = None


def local_demo() -> dict[str, Any]:
    """Demo sin cliente MCP: permite explicar schemas/scopes aunque no se lance Antigravity."""
    ctx = load_auth_context()
    legacy = TicketV1(customer_id="cus_123", issue="Mi pedido llego tarde y necesito ayuda")
    migrated = migrate_ticket_v1_to_v2(legacy)
    try:
        TicketV2.model_validate({"customer_id": "cus_123", "issue": "corto", "priority": "urgent"})
    except ValidationError as exc:
        validation_error = str(exc)
    else:
        validation_error = "sin_error"
    return {
        "trusted_context": ctx.model_dump(mode="json"),
        "legacy_payload": legacy.model_dump(mode="json"),
        "migrated_payload": migrated.model_dump(mode="json"),
        "validation_error": validation_error,
        "audit_log_path": str(AUDIT_LOG_PATH),
    }


def main() -> None:
    """Por defecto ejecuta como server MCP por STDIO."""
    if mcp is None:
        raise RuntimeError('Falta instalar la dependencia MCP: pip install "mcp[cli]>=1.27,<2"')
    mcp.run()


if __name__ == "__main__":
    main()
