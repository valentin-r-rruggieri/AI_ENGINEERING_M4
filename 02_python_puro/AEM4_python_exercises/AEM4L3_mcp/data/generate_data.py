"""Genera datasets JSON para AEM4L3 MCP."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common import write_json

DATA_DIR = Path(__file__).parent


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    write_json(DATA_DIR / "catalogo_productos.json", [
        {"sku": "AUD-100", "nombre": "Auriculares Bluetooth Pro", "categoria": "audio", "precio": 89000, "stock": 12},
        {"sku": "AUD-200", "nombre": "Auriculares Cableados Studio", "categoria": "audio", "precio": 32000, "stock": 34},
        {"sku": "TEC-010", "nombre": "Teclado Mecanico Compacto", "categoria": "perifericos", "precio": 76000, "stock": 8},
        {"sku": "MOU-020", "nombre": "Mouse Ergonomico Vertical", "categoria": "perifericos", "precio": 41000, "stock": 19},
        {"sku": "MON-144", "nombre": "Monitor 27 pulgadas 144Hz", "categoria": "monitores", "precio": 310000, "stock": 5},
        {"sku": "CAM-030", "nombre": "Webcam Full HD", "categoria": "video", "precio": 52000, "stock": 15},
        {"sku": "DOC-001", "nombre": "Dock USB C Empresarial", "categoria": "conectividad", "precio": 118000, "stock": 7},
        {"sku": "MIC-050", "nombre": "Microfono Condenser USB", "categoria": "audio", "precio": 99000, "stock": 4},
    ])

    tools_registry = [
        {
            "name": "buscar_producto",
            "description": "Busca productos por nombre, SKU o categoria.",
            "input_schema": {"query": "string", "limit": "integer opcional"},
            "output_schema": {"results": "list[producto]"},
            "required_scope": "catalogo:producto:leer",
        },
        {
            "name": "consultar_precio",
            "description": "Consulta precio y stock de un SKU.",
            "input_schema": {"sku": "string"},
            "output_schema": {"sku": "string", "precio": "number", "stock": "integer"},
            "required_scope": "catalogo:precio:leer",
        },
        {
            "name": "crear_pedido",
            "description": "Crea un pedido para un cliente.",
            "input_schema": {"sku": "string", "cantidad": "integer", "cliente_id": "string"},
            "output_schema": {"pedido_id": "string", "status": "string"},
            "required_scope": "ventas:pedido:crear",
        },
        {
            "name": "actualizar_salario",
            "description": "Actualiza salario de un empleado.",
            "input_schema": {"empleado_id": "string", "nuevo_salario": "number"},
            "output_schema": {"empleado_id": "string", "status": "string"},
            "required_scope": "rrhh:salario:actualizar",
        },
        {
            "name": "transferir_fondos",
            "description": "Transfiere fondos entre cuentas.",
            "input_schema": {"monto": "number", "cuenta_destino": "string", "moneda": "string"},
            "output_schema": {"transferencia_id": "string", "status": "string"},
            "required_scope": "banco:fondos:transferir",
        },
    ]
    write_json(DATA_DIR / "tools_registry.json", tools_registry)

    write_json(DATA_DIR / "roles_scopes.json", {
        "viewer": ["catalogo:producto:leer", "catalogo:precio:leer"],
        "operator": ["catalogo:producto:leer", "catalogo:precio:leer", "ventas:pedido:*"],
        "admin": ["catalogo:*:*", "ventas:*:*", "rrhh:*:*", "banco:*:*"],
    })

    write_json(DATA_DIR / "tool_schema_v1.json", {
        "name": "transferir_fondos",
        "version": "1.0.0",
        "input_schema": {
            "monto": {"type": "string", "required": True},
            "cuenta_destino": {"type": "string", "required": True},
        },
    })
    write_json(DATA_DIR / "tool_schema_v2.json", {
        "name": "transferir_fondos",
        "version": "2.0.0",
        "input_schema": {
            "monto": {"type": "float", "required": True},
            "cuenta_destino": {"type": "string", "required": True},
            "moneda": {"type": "string", "required": True},
        },
    })

    print(f"Dataset L3 generado en: {DATA_DIR}")


if __name__ == "__main__":
    main()
