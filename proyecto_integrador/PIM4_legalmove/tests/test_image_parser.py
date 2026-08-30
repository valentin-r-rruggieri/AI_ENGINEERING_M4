"""Pruebas aisladas del parsing de imágenes, sin llamadas a OpenAI."""

# Importa objetos simples, Pillow y pytest para simular la Responses API.
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

from src.config import Settings
from src.errors import ImageValidationError, VisionParsingError
from src.image_parser import encode_image_to_base64, parse_contract_image, validate_image_path


# Construye una configuración segura con valores ficticios para las pruebas.
def configuracion() -> Settings:
    return Settings("key", "gpt-4o", "gpt-4o", "pk", "sk", "https://host", 10, 0)


# Simula el cliente OpenAI y registra los argumentos de la llamada.
class ClienteFalso:
    def __init__(self, texto: str) -> None:
        self.texto = texto
        self.arguments = {}
        self.responses = SimpleNamespace(create=self.create)

    def create(self, **kwargs):
        self.arguments = kwargs
        return SimpleNamespace(
            output_text=self.texto,
            usage=SimpleNamespace(input_tokens=10, output_tokens=5),
        )


# Guarda los datos enviados a la generación Langfuse simulada.
class ObservacionFalsa:
    def __init__(self) -> None:
        self.actualizaciones = []

    def update(self, **kwargs) -> None:
        self.actualizaciones.append(kwargs)


# Crea una imagen válida pequeña para no depender de archivos externos.
def crear_png(ruta: Path) -> None:
    Image.new("RGB", (20, 20), "white").save(ruta)


# Verifica Base64, MIME y el payload multimodal enviado al cliente.
def test_extrae_texto_y_envia_imagen_base64(tmp_path: Path) -> None:
    ruta = tmp_path / "contrato.png"
    crear_png(ruta)
    cliente = ClienteFalso("CLÁUSULA 1 - Texto fiel")
    observacion = ObservacionFalsa()
    texto = parse_contract_image(
        ruta,
        "Contrato original",
        settings=configuracion(),
        client=cliente,
        observation=observacion,
    )

    assert texto == "CLÁUSULA 1 - Texto fiel"
    assert cliente.arguments["model"] == "gpt-4o"
    imagen = cliente.arguments["input"][0]["content"][1]
    assert imagen["image_url"].startswith("data:image/png;base64,")
    assert imagen["detail"] == "high"
    assert encode_image_to_base64(ruta, 1024 * 1024)[1] == "image/png"
    assert observacion.actualizaciones[-1]["usage_details"] == {
        "input": 10,
        "output": 5,
        "total": 15,
    }


# Verifica rutas inexistentes, formatos inválidos, corrupción y respuestas vacías.
def test_rechaza_entradas_invalidas_y_respuesta_vacia(tmp_path: Path) -> None:
    with pytest.raises(ImageValidationError):
        validate_image_path(tmp_path / "ausente.png", 1000)

    archivo_texto = tmp_path / "contrato.txt"
    archivo_texto.write_text("no es imagen", encoding="utf-8")
    with pytest.raises(ImageValidationError):
        validate_image_path(archivo_texto, 1000)

    corrupta = tmp_path / "corrupta.png"
    corrupta.write_bytes(b"no es una imagen")
    with pytest.raises(ImageValidationError):
        validate_image_path(corrupta, 1000)

    valida = tmp_path / "valida.png"
    crear_png(valida)
    with pytest.raises(VisionParsingError):
        parse_contract_image(valida, "Contrato", settings=configuracion(), client=ClienteFalso("  "))
