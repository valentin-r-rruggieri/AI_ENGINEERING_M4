"""Genera datasets de texto para AEM4L4."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common import write_json

DATA_DIR = Path(__file__).parent


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    (DATA_DIR / "oracion_ejemplo.txt").write_text(
        "El banco del parque estaba mojado por la lluvia.",
        encoding="utf-8",
    )
    (DATA_DIR / "nota_medica.txt").write_text(
        "Paciente con hipertension arterial controlada. Indicar losartan 50 mg cada 24 horas "
        "y controlar presion durante siete dias. Si presenta mareos, ajustar dosis y consultar.",
        encoding="utf-8",
    )
    contrato = (
        "Contrato de prestacion de servicios profesionales. La empresa contratante encomienda al proveedor "
        "la ejecucion de tareas de soporte tecnico, mantenimiento preventivo y documentacion operativa. "
        "El proveedor debera entregar reportes mensuales con indicadores de disponibilidad, incidentes "
        "resueltos, tiempos de respuesta y riesgos detectados. El pago mensual sera realizado dentro de "
        "los diez dias habiles posteriores a la recepcion de la factura. La confidencialidad se mantendra "
        "durante toda la relacion contractual y por tres anios posteriores a su finalizacion. En caso de "
        "incumplimiento grave, la parte afectada podra rescindir el contrato con preaviso fehaciente de "
        "treinta dias. Las obligaciones de seguridad de la informacion incluyen control de accesos, "
        "registro de cambios, resguardo de credenciales y reporte inmediato de vulnerabilidades. "
    )
    (DATA_DIR / "contrato_legal.txt").write_text(contrato * 4, encoding="utf-8")

    write_json(DATA_DIR / "perfiles_uso.json", [
        {"cliente": "legal_enterprise", "dominios": ["legal"], "presupuesto": "alto", "trafico": "estable_alto"},
        {"cliente": "multi_tenant_saas", "dominios": ["legal", "finanzas", "rrhh"], "presupuesto": "medio", "trafico": "variable"},
        {"cliente": "startup_medica", "dominios": ["medicina"], "presupuesto": "bajo", "trafico": "bajo"},
        {"cliente": "plataforma_regional", "dominios": ["legal", "compliance"], "presupuesto": "alto", "trafico": "picos"},
    ])

    write_json(DATA_DIR / "chatbot_financiero.json", {
        "company": "Banco Regional",
        "goal": "Responder preguntas de clientes sobre productos, limites y requisitos regulatorios.",
        "latency_sla_ms": 600,
        "gpu_budget": "limitado",
        "domain_terms": [
            "perfil transaccional",
            "sujeto obligado",
            "debida diligencia reforzada",
            "riesgo crediticio",
            "microfinanciamiento",
        ],
        "sample_context": [
            "El cliente consulta si puede aumentar el limite de su tarjeta adicional.",
            "La politica interna exige revisar historial crediticio, ingresos declarados y alertas AML.",
            "La normativa nueva agrega controles para sujetos obligados y operaciones inusuales.",
        ],
        "expected_decisions": [
            "Transformer moderado por balance de calidad y latencia.",
            "Tokenizacion subword robusta para jerga financiera y regulatoria.",
            "LoRA para adaptar dominio sin reentrenar todos los parametros.",
            "Contexto controlado con recuperacion de documentos relevantes.",
        ],
    })

    print(f"Dataset L4 generado en: {DATA_DIR}")


if __name__ == "__main__":
    main()
