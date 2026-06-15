"""
E01 - Tool calling ad hoc vs contrato MCP con LangChain
AEM4L3 | Model Context Protocol

Objetivo pedagogico:
    Mostrar por que describir herramientas como texto libre obliga a parsear
    strings fragiles, y como un contrato estilo MCP permite tool calls
    estructurados, argumentos validados y ejecucion auditable.

Flujo:
    catalogo_productos.json + tools_registry.json
    -> version basica con texto libre
    -> version mejorada con tool_call estructurado y Pydantic

USE_REAL_API = False:
    Lee los JSON reales y simula el tool_call que devolveria LangChain.
USE_REAL_API = True:
    Usa ChatOpenAI.bind_tools() para que el modelo elija la tool.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import print_file_evidence, print_section, print_title, read_json, run_generator

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
CATALOG_PATH = DATA_DIR / "catalogo_productos.json"
TOOLS_PATH = DATA_DIR / "tools_registry.json"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", CATALOG_PATH)


class BuscarProductoArgs(BaseModel):
    query: str = Field(..., min_length=2, description="Nombre, SKU o categoria")
    limit: int = Field(10, ge=1, le=20, description="Maximo de resultados")


class ConsultarPrecioArgs(BaseModel):
    sku: str = Field(..., min_length=3)


def buscar_producto(catalogo: list[dict[str, Any]], query: str, limit: int = 10) -> list[dict[str, Any]]:
    q = query.lower()
    return [
        p for p in catalogo
        if q in p["sku"].lower() or q in p["nombre"].lower() or q in p["categoria"].lower()
    ][:limit]


def consultar_precio(catalogo: list[dict[str, Any]], sku: str) -> dict[str, Any]:
    for producto in catalogo:
        if producto["sku"].lower() == sku.lower():
            return {"sku": producto["sku"], "precio": producto["precio"], "stock": producto["stock"]}
    return {"error": "sku_no_encontrado", "sku": sku}


def ad_hoc_tool_use(user_query: str) -> str:
    if USE_REAL_API:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Si el usuario pregunta por productos devolve BUSCAR: <nombre>. Si pregunta precio devolve PRECIO: <sku>."),
            ("user", "{query}"),
        ])
        chain = prompt | ChatOpenAI(model=MODEL_NAME, temperature=0) | StrOutputParser()
        return chain.invoke({"query": user_query})
    print("  [MOCK] Simulando salida libre del modelo...")
    return "Buscar producto: auriculares, maximo cinco resultados"


def parse_ad_hoc_output(text: str) -> dict[str, Any]:
    match = re.search(r"BUSCAR:\s*(.+)", text, flags=re.IGNORECASE)
    if match:
        return {"tool": "buscar_producto", "query": match.group(1).strip(), "limit": 10}
    return {"error": "no_pude_parsear", "raw": text}


def langchain_tool_call(user_query: str) -> dict[str, Any]:
    if USE_REAL_API:
        from langchain_core.tools import tool
        from langchain_openai import ChatOpenAI

        @tool(args_schema=BuscarProductoArgs)
        def buscar_producto_tool(query: str, limit: int = 10) -> list:
            """Busca productos en el catalogo por nombre, SKU o categoria."""
            return []

        @tool(args_schema=ConsultarPrecioArgs)
        def consultar_precio_tool(sku: str) -> dict:
            """Consulta precio y stock de un SKU."""
            return {}

        llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
        msg = llm.bind_tools([buscar_producto_tool, consultar_precio_tool]).invoke(user_query)
        return msg.tool_calls[0] if msg.tool_calls else {"name": "sin_tool", "args": {}}

    print("  [MOCK] Simulando AIMessage.tool_calls de LangChain...")
    return {"name": "buscar_producto", "args": {"query": "auriculares", "limit": 5}}


def execute_tool_call(catalogo: list[dict[str, Any]], tool_call: dict[str, Any]) -> Any:
    if tool_call["name"] == "buscar_producto":
        args = BuscarProductoArgs(**tool_call["args"])
        return buscar_producto(catalogo, args.query, args.limit)
    if tool_call["name"] == "consultar_precio":
        args = ConsultarPrecioArgs(**tool_call["args"])
        return consultar_precio(catalogo, args.sku)
    return {"error": "tool_desconocida", "tool_call": tool_call}


def main() -> None:
    ensure_data()
    catalogo = read_json(CATALOG_PATH)
    tools = read_json(TOOLS_PATH)

    print_title("AEM4L3 | E01 - Tool calling ad hoc vs contrato MCP")

    print_section(1, "CONTEXTO DEL CASO")
    print("Un ecommerce quiere que un LLM consulte productos sin inventar formatos.")
    print_file_evidence(CATALOG_PATH, "Resource catalogo")
    print_file_evidence(TOOLS_PATH, "Registry MCP")
    print(f"Productos cargados: {len(catalogo)}")

    print_section(2, "VERSION BASICA - tools como texto libre")
    query = "Necesito auriculares, mostrame opciones disponibles."
    libre = ad_hoc_tool_use(query)
    print(f"Query usuario: {query}")
    print(f"Salida libre: {libre}")
    print(f"Parser regex/split: {parse_ad_hoc_output(libre)}")

    print_section(3, "PROBLEMA DETECTADO")
    print("Sin contrato no hay input_schema, no hay validacion de argumentos y el parser depende del estilo del modelo.")
    print("El modelo escribio 'Buscar producto:' en vez de 'BUSCAR:', entonces el parseo ya quedo fragil.")

    print_section(4, "VERSION MEJORADA - MCP + LangChain bind_tools")
    print("Anatomia del contrato MCP leida desde tools_registry.json:")
    for tool in tools[:2]:
        print(f"  - {tool['name']}: input={tool['input_schema']} output={tool['output_schema']} scope={tool['required_scope']}")
    tool_call = langchain_tool_call(query)
    print(f"Tool call estructurado: {tool_call}")
    resultado = execute_tool_call(catalogo, tool_call)
    print(f"Resultado ejecutado contra catalogo real: {resultado}")
    print("Primitivas: buscar_producto=Tool | catalogo_productos.json=Resource | template_respuesta_cliente=Prompt")

    print_section(5, "VALIDACION")
    try:
        BuscarProductoArgs(query="auriculares", limit="cinco")
    except ValidationError as exc:
        print("Pydantic rechaza limit no entero:")
        print(exc)
    print(f"Forma estable del tool_call: name={tool_call.get('name')} args={tool_call.get('args')}")

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: string libre -> regex fragil -> argumentos sin schema -> ejecucion incierta.")
    print("DESPUES: tool_call {name,args} -> Pydantic -> contrato MCP explicito -> ejecucion verificable.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega crear_pedido con required_scope ventas:pedido:crear.")
    print("2. Explica por que crear_pedido requiere mas privilegios que buscar_producto.")
    print("3. Clasifica tres elementos nuevos como Tool, Resource o Prompt.")


if __name__ == "__main__":
    main()
