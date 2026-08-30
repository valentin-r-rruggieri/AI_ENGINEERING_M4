"""Pruebas del orden de etapas y la entrega del mapa al segundo agente."""

# Importa contextmanager, rutas y el pipeline sin inicializar servicios reales.
from contextlib import contextmanager
from pathlib import Path

from PIL import Image

from src.config import Settings
from src.models import ContractChangeOutput
from src.pipeline import analyze_contracts


# Simula un span Langfuse que guarda sus actualizaciones para poder inspeccionarlas.
class SpanFalso:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.updates = []

    def update(self, **kwargs) -> None:
        self.updates.append(kwargs)


# Simula observabilidad sin enviar trazas a internet.
class ObservabilidadFalsa:
    def __init__(self) -> None:
        self.nombres = []
        self.flush_llamado = False

    @contextmanager
    def observation(self, *, name, **kwargs):
        self.nombres.append(name)
        yield SpanFalso(name)

    def callback_handler(self):
        return object()

    def flush(self) -> None:
        self.flush_llamado = True


# Entrega un contexto verificable y un extractor que exige recibirlo.
class ContextoFalso:
    def run(self, original, adenda, callbacks=None):
        return "Mapa contextual entregado"


class ExtractorFalso:
    def __init__(self) -> None:
        self.contexto = ""

    def run(self, original, adenda, contexto, callbacks=None):
        self.contexto = contexto
        return ContractChangeOutput(
            sections_changed=["Cláusula 2"],
            topics_touched=["precio"],
            summary_of_the_change="MODIFICACIÓN: el precio cambia de acuerdo con la adenda presentada.",
        )


# Ejecuta exactamente las cinco etapas esperadas sin consumir APIs reales.
def test_pipeline_respeta_orden_y_handoff(tmp_path: Path) -> None:
    original = tmp_path / "original.png"
    adenda = tmp_path / "adenda.png"
    Image.new("RGB", (10, 10), "white").save(original)
    Image.new("RGB", (10, 10), "white").save(adenda)
    observabilidad = ObservabilidadFalsa()
    extractor = ExtractorFalso()

    def parser(ruta, etiqueta, **kwargs):
        return f"Texto de {etiqueta}"

    configuracion = Settings("key", "gpt-4o", "gpt-4o", "pk", "sk", "https://host", 10, 0)
    resultado = analyze_contracts(
        original,
        adenda,
        settings=configuracion,
        image_parser=parser,
        contextualization_agent=ContextoFalso(),
        extraction_agent=extractor,
        observability=observabilidad,
        openai_client=object(),
    )
    assert observabilidad.nombres == [
        "contract-analysis",
        "parse_original_contract",
        "parse_amendment_contract",
        "contextualization_agent",
        "extraction_agent",
        "pydantic_validation",
    ]
    assert extractor.contexto == "Mapa contextual entregado"
    assert resultado.output.sections_changed == ["Cláusula 2"]
    assert observabilidad.flush_llamado is True
