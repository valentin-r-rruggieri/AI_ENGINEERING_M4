"""
E01 - Self-attention conceptual + structured output
AEM4L4 | Fundamentos teoricos y arquitectura

Objetivo pedagogico:
    Entender que cada token puede mirar a todos los demas, visualizar una
    matriz NxN y contrastar texto libre vs DependencyMap estructurado.

USE_REAL_API = False:
    Lee textos reales y usa mocks calibrados.
USE_REAL_API = True:
    Usa LangChain structured output para extraer dependencias.
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path
from typing import List

import numpy as np
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import print_file_evidence, print_section, print_title, read_text, run_generator

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
SENTENCE_PATH = DATA_DIR / "oracion_ejemplo.txt"
MEDICAL_PATH = DATA_DIR / "nota_medica.txt"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", SENTENCE_PATH)


class AttentionLink(BaseModel):
    token: str
    attends_to: str
    reason: str = Field(..., min_length=5)


class DependencyMap(BaseModel):
    sentence: str
    links: List[AttentionLink] = Field(..., min_length=1)


def softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def simulated_attention(tokens: list[str]) -> np.ndarray:
    scores = np.ones((len(tokens), len(tokens))) * 0.1
    for i, token in enumerate(tokens):
        for j, other in enumerate(tokens):
            if token.lower().startswith("banco") and other.lower().startswith("parque"):
                scores[i, j] = 4.0
            if token.lower().startswith("mojado") and other.lower().startswith("lluvia"):
                scores[i, j] = 4.0
            if i == j:
                scores[i, j] += 1.0
    return softmax(scores)


def print_matrix(tokens: list[str], matrix: np.ndarray) -> None:
    header = "          " + " ".join(f"{t[:7]:>8}" for t in tokens)
    print(header)
    for token, row in zip(tokens, matrix):
        print(f"{token[:8]:>8} " + " ".join(f"{v:8.2f}" for v in row))


def qkv_demo(tokens: list[str]) -> np.ndarray:
    rng = np.random.default_rng(7)
    d = 4
    embeddings = rng.normal(size=(len(tokens), d))
    q = embeddings @ rng.normal(size=(d, d))
    k = embeddings @ rng.normal(size=(d, d))
    v = embeddings @ rng.normal(size=(d, d))
    attn = softmax((q @ k.T) / math.sqrt(d))
    output = attn @ v
    print("Formula: softmax(Q.K^T / sqrt(d)) . V")
    print(f"Shapes: Q={q.shape} K={k.shape} V={v.shape} output={output.shape}")
    return attn


def extract_dependencies(sentence: str) -> DependencyMap:
    if USE_REAL_API:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI

        class _DependencyMap(DependencyMap):
            pass

        llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Extrae dependencias de atencion semantica entre palabras. Devolve schema estricto."),
            ("user", "{sentence}"),
        ])
        chain = prompt | llm.with_structured_output(_DependencyMap)
        return chain.invoke({"sentence": sentence})
    if "hipertension" in sentence.lower():
        return DependencyMap(sentence=sentence, links=[
            AttentionLink(token="hipertension", attends_to="losartan", reason="tratamiento indicado"),
            AttentionLink(token="dosis", attends_to="50 mg", reason="cantidad que se administra"),
            AttentionLink(token="controlar", attends_to="presion", reason="variable clinica a seguir"),
        ])
    return DependencyMap(sentence=sentence, links=[
        AttentionLink(token="banco", attends_to="parque", reason="resuelve que banco es asiento"),
        AttentionLink(token="mojado", attends_to="lluvia", reason="explica la causa del estado"),
    ])


def main() -> None:
    ensure_data()
    sentence = read_text(SENTENCE_PATH)
    medical = read_text(MEDICAL_PATH)
    tokens = sentence.replace(".", "").split()

    print_title("AEM4L4 | E01 - Self-attention conceptual")

    print_section(1, "CONTEXTO DEL CASO")
    print_file_evidence(SENTENCE_PATH, "Oracion")
    print_file_evidence(MEDICAL_PATH, "Nota medica")
    print(f"Oracion: {sentence}")

    print_section(2, "VERSION BASICA - intuicion y texto libre")
    attn = simulated_attention(tokens)
    print("Mapa NxN simulado: cada fila suma 1.0 y muestra a que mira cada token.")
    print_matrix(tokens, attn)
    print("Texto libre del LLM: 'banco se relaciona con parque y mojado con lluvia' -> util para leer, dificil para graficar.")

    print_section(3, "PROBLEMA DETECTADO")
    print("El texto libre no es indexable. Para graficar o auditar necesito pares token -> attends_to con motivo.")

    print_section(4, "VERSION MEJORADA - Q/K/V + structured output")
    qkv_demo(tokens)
    dep = extract_dependencies(sentence)
    print(f"DependencyMap: {dep}")
    dep_medica = extract_dependencies(medical)
    print(f"Caso medico: {dep_medica}")

    print_section(5, "VALIDACION")
    print(f"Suma de filas softmax: {[round(x, 4) for x in attn.sum(axis=1)]}")
    try:
        DependencyMap(sentence=sentence, links=[{"token": "banco", "attends_to": "parque"}])
    except ValidationError as exc:
        print("Pydantic rechaza link sin reason:")
        print(exc)

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: lectura secuencial o texto libre; dificil conectar y auditar relaciones.")
    print("DESPUES: attention NxN + DependencyMap estructurado e indexable.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Cambia la oracion por 'El gato vio el raton porque tenia hambre'.")
    print("2. Decide si 'tenia' atiende a gato o raton y justifica.")
    print("3. Genera un mapa similar para otra nota medica.")


if __name__ == "__main__":
    main()
