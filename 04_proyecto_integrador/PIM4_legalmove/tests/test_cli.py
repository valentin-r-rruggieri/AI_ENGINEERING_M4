"""Pruebas de la interfaz de línea de comandos, sin credenciales reales."""

# Importa el módulo principal y los objetos necesarios para simular el pipeline.
from src import main as cli
from src.config import Settings
from src.errors import ConfigurationError
from src.models import ContractChangeOutput, PipelineResult


# Comprueba que stdout contiene solamente el JSON validado.
def test_cli_imprime_json(monkeypatch, capsys) -> None:
    configuracion = Settings("key", "gpt-4o", "gpt-4o", "pk", "sk", "https://host", 10, 0)
    salida = ContractChangeOutput(
        sections_changed=["Cláusula 2"],
        topics_touched=["precio"],
        summary_of_the_change="MODIFICACIÓN: el precio del contrato se actualiza por la adenda.",
    )
    resultado = PipelineResult(salida, "original", "adenda", "mapa")
    monkeypatch.setattr(cli.Settings, "from_env", lambda: configuracion)
    monkeypatch.setattr(cli, "analyze_contracts", lambda *args, **kwargs: resultado)

    assert cli.main(["original.png", "adenda.png"]) == 0
    capturado = capsys.readouterr()
    assert '"sections_changed"' in capturado.out
    assert capturado.err == ""


# Comprueba que una configuración inválida se informa por stderr y falla.
def test_cli_informa_error_de_configuracion(monkeypatch, capsys) -> None:
    def fallar():
        raise ConfigurationError("Falta OPENAI_API_KEY")

    monkeypatch.setattr(cli.Settings, "from_env", fallar)
    assert cli.main(["original.png", "adenda.png"]) == 1
    capturado = capsys.readouterr()
    assert capturado.out == ""
    assert "Falta OPENAI_API_KEY" in capturado.err
