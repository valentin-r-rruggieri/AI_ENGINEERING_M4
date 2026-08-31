"""
E04 - Vocabulario, latencia y budget de contexto
AEM4L4 | Fundamentos teoricos y arquitectura

Objetivo pedagogico:
    Calcular como crece attention con N tokens, estimar latencia relativa y
    decidir estrategias para cumplir un SLA sin esconder el trade-off.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Scenario:
    name: str
    tokens: int
    tokenizer: str
    description: str


def title(text: str) -> None:
    print("\n" + "=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print(f"\n{number}. {text}")
    print("-" * 78)


def attention_pairs(tokens: int) -> int:
    return tokens * tokens


def relative_latency_ms(tokens: int, base_tokens: int = 100, base_ms: int = 120) -> float:
    return base_ms * attention_pairs(tokens) / attention_pairs(base_tokens)


def recommend_strategy(tokens: int, sla_ms: int) -> list[str]:
    latency = relative_latency_ms(tokens)
    strategies = []
    if latency > sla_ms:
        strategies.extend(["limitar input", "recuperar solo documentos relevantes", "resumir contexto"])
    if tokens > 1000:
        strategies.append("chunking con ranking")
    if tokens > 3000:
        strategies.append("modelo/contexto especializado o pipeline asincronico")
    if not strategies:
        strategies.append("mantener contexto actual y medir con trafico real")
    return strategies


def main() -> None:
    scenarios = [
        Scenario("A", 10, "subword robusto", "Pregunta corta"),
        Scenario("B", 30, "subword robusto", "Consulta con detalles"),
        Scenario("C", 50, "wordpiece", "Texto tecnico moderado"),
        Scenario("D", 100, "bpe", "Prompt largo para demo"),
        Scenario("E", 1200, "subword fragmentado", "Contrato legal con clausulas"),
    ]
    sla_ms = 600

    title("AEM4L4 | E04 - Vocabulario y latencia")

    section(1, "Tabla de costo")
    print(f"{'Esc':<4} {'Tokens':>8} {'Pares attention':>18} {'Latencia rel.':>15}  Tokenizer")
    for scenario in scenarios:
        print(
            f"{scenario.name:<4} {scenario.tokens:>8} {attention_pairs(scenario.tokens):>18} "
            f"{relative_latency_ms(scenario.tokens):>12.0f} ms  {scenario.tokenizer}"
        )

    section(2, "Decision contra SLA")
    for scenario in scenarios:
        latency = relative_latency_ms(scenario.tokens)
        status = "OK" if latency <= sla_ms else "RIESGO"
        print(f"{scenario.name}: {status} ({latency:.0f} ms estimados, SLA {sla_ms} ms)")
        print("  Estrategias:", ", ".join(recommend_strategy(scenario.tokens, sla_ms)))

    section(3, "Interpretacion")
    print("Duplicar tokens cuadruplica pares de attention. Mas contexto puede traer mas ruido y mas costo.")
    print("Un vocabulario chico ahorra embeddings, pero puede fragmentar palabras y aumentar tokens.")

    section(4, "Desafio")
    print("Agrega un escenario de 4000 tokens y propone un plan para bajarlo debajo del SLA.")


if __name__ == "__main__":
    main()
