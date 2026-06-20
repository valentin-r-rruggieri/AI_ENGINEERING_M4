"""
E01 - Self-attention conceptual + Q/K/V + structured output
AEM4L4 | Fundamentos teoricos y arquitectura

Objetivo pedagogico:
    Ver que cada token puede mirar a todos los demas, imprimir una matriz
    NxN interpretable y pedir a OpenAI una extraccion estructurada de
    dependencias semanticas.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import List, cast

import numpy as np
from dotenv import load_dotenv
from pydantic import BaseModel, Field


DATA_DIR = Path(__file__).parent / "data"
SENTENCE_PATH = DATA_DIR / "oracion_ejemplo.txt"
MEDICAL_PATH = DATA_DIR / "nota_medica.txt"


class AttentionLink(BaseModel):
    token: str
    attends_to: str
    reason: str = Field(..., min_length=5)


class DependencyMap(BaseModel):
    sentence: str
    links: List[AttentionLink] = Field(..., min_length=1)


def title(text: str) -> None:
    print("\n" + "=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print(f"\n{number}. {text}")
    print("-" * 78)


def ensure_data() -> None:
    if SENTENCE_PATH.exists() and MEDICAL_PATH.exists():
        return
    subprocess.run([sys.executable, str(DATA_DIR / "generate_data.py")], check=True)


def require_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Falta OPENAI_API_KEY. Copia python_puro/AEM4_python_exercises/.env.example "
            "a .env y completa tu API key antes de ejecutar este ejercicio."
        )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def simulated_attention(tokens: list[str]) -> np.ndarray:
    scores = np.ones((len(tokens), len(tokens))) * 0.1
    for i, token in enumerate(tokens):
        for j, other in enumerate(tokens):
            token_l = token.lower().strip(".,;:")
            other_l = other.lower().strip(".,;:")
            if token_l == "banco" and other_l in {"parque", "mojado"}:
                scores[i, j] = 4.0
            if token_l == "mojado" and other_l in {"lluvia", "banco"}:
                scores[i, j] = 4.0
            if i == j:
                scores[i, j] += 1.0
    return softmax(scores)


def print_matrix(tokens: list[str], matrix: np.ndarray) -> None:
    header = "token".rjust(11) + " " + " ".join(f"{token[:8]:>8}" for token in tokens)
    print(header)
    for token, row in zip(tokens, matrix):
        values = " ".join(f"{value:8.2f}" for value in row)
        print(f"{token[:10]:>11} {values}")


def qkv_shapes(tokens: list[str]) -> np.ndarray:
    rng = np.random.default_rng(7)
    d_model = 4
    embeddings = rng.normal(size=(len(tokens), d_model))
    w_q = rng.normal(size=(d_model, d_model))
    w_k = rng.normal(size=(d_model, d_model))
    w_v = rng.normal(size=(d_model, d_model))
    q = embeddings @ w_q
    k = embeddings @ w_k
    v = embeddings @ w_v
    attention = softmax((q @ k.T) / math.sqrt(d_model))
    output = attention @ v
    print("Formula: softmax(Q @ K.T / sqrt(d_model)) @ V")
    print(f"Embeddings={embeddings.shape} Q={q.shape} K={k.shape} V={v.shape} Output={output.shape}")
    return attention


def extract_dependencies(sentence: str) -> DependencyMap:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Extrae dependencias de self-attention semantica. "
                "Usa pares token -> attends_to y una razon breve en espanol.",
            ),
            ("user", "{sentence}"),
        ]
    )
    chain = prompt | ChatOpenAI(model=model_name, temperature=0).with_structured_output(DependencyMap)
    return cast(DependencyMap, chain.invoke({"sentence": sentence}))


def main() -> None:
    load_dotenv()
    ensure_data()
    require_openai_api_key()

    sentence = read_text(SENTENCE_PATH)
    medical = read_text(MEDICAL_PATH)
    tokens = sentence.replace(".", "").split()

    title("AEM4L4 | E01 - Self-attention conceptual")

    section(1, "Contexto")
    print(f"Oracion base: {sentence}")
    print(f"Nota medica: {medical}")

    section(2, "Mapa de atencion simulado")
    attention = simulated_attention(tokens)
    print_matrix(tokens, attention)
    print("Cada fila representa un token mirando a todos los otros tokens. Cada fila suma 1.0.")

    section(3, "Q/K/V minimo")
    qkv_attention = qkv_shapes(tokens)
    print("Primer fila de attention Q/K/V:", [round(float(x), 3) for x in qkv_attention[0]])

    section(4, "OpenAI structured output")
    dependency_map = extract_dependencies(sentence)
    medical_map = extract_dependencies(medical)
    print(json.dumps(dependency_map.model_dump(mode="json"), ensure_ascii=False, indent=2))
    print(json.dumps(medical_map.model_dump(mode="json"), ensure_ascii=False, indent=2))

    section(5, "Desafio")
    print("Cambia la oracion por una frase ambigua y compara que tokens reciben mas atencion.")


if __name__ == "__main__":
    main()
