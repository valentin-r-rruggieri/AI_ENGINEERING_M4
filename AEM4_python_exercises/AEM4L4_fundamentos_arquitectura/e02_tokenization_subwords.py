"""
E02 - Tokenizacion subword y costo de contexto
AEM4L4 | Fundamentos teoricos y arquitectura

Objetivo pedagogico:
    Mostrar por que word-level produce [UNK], como BPE/WordPiece reconstruyen
    terminos raros y por que mas tokens implican mas costo O(N^2).

USE_REAL_API = False/True:
    Este ejercicio no necesita LLM para el nucleo matematico; siempre usa data local.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from common import print_file_evidence, print_section, print_title, read_text, run_generator, trace_json, trace_text


def print(*args, **kwargs):  # type: ignore[no-untyped-def]
    return None

load_dotenv()

USE_REAL_API = False
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATA_DIR = Path(__file__).parent / "data"
LEGAL_PATH = DATA_DIR / "contrato_legal.txt"


def ensure_data() -> None:
    run_generator(DATA_DIR, "generate_data.py", LEGAL_PATH)


VOCAB = {"contrato", "pago", "monto", "plazo", "paciente", "banco", "la", "el", "de", "servicios"}


def word_tokenize(word: str) -> list[str]:
    return [word] if word.lower() in VOCAB else ["[UNK]"]


def char_tokenize(word: str) -> list[str]:
    return list(word)


def fake_bpe(word: str) -> list[str]:
    mapping = {
        "hipercolesterolemia": ["hiper", "colesterol", "emia"],
        "responsabilidadcontractual": ["responsabilidad", "contract", "ual"],
        "microfinanciamiento": ["micro", "financ", "iamiento"],
        "electroencefalograma": ["electro", "encefalo", "grama"],
        "confidencialidad": ["confidencial", "idad"],
    }
    return mapping.get(word.lower(), [word[i:i + 5] for i in range(0, len(word), 5)])


def fake_wordpiece(word: str) -> list[str]:
    pieces = fake_bpe(word)
    return pieces[:1] + [f"##{p}" for p in pieces[1:]]


class TokenBudget(BaseModel):
    name: str
    tokens: int = Field(..., gt=0)
    attention_pairs: int = Field(..., gt=0)


@dataclass
class TokenizationRow:
    word: str
    word_level: list[str]
    char_level: list[str]
    bpe: list[str]
    wordpiece: list[str]


def main() -> None:
    ensure_data()
    contrato = read_text(LEGAL_PATH)
    technical_words = ["hipercolesterolemia", "responsabilidadcontractual", "microfinanciamiento", "electroencefalograma", "confidencialidad"]

    print_title("AEM4L4 | E02 - Tokenizacion subword")

    print_section(1, "CONTEXTO DEL CASO")
    print("Medicina, derecho y finanzas tienen palabras que no entran en un vocabulario comun.")
    print_file_evidence(LEGAL_PATH, "Contrato legal")
    print(f"Preview: {contrato[:180]}...")

    print_section(2, "VERSION BASICA - word-level")
    for word in technical_words:
        print(f"  {word:<32} -> {word_tokenize(word)}")

    print_section(3, "PROBLEMA DETECTADO")
    print("[UNK] borra informacion. El modelo no ve prefijos, raices ni sufijos tecnicos.")
    print("Character-level no pierde informacion, pero hace secuencias larguisimas.")

    print_section(4, "VERSION MEJORADA - BPE y WordPiece")
    rows = [
        TokenizationRow(w, word_tokenize(w), char_tokenize(w), fake_bpe(w), fake_wordpiece(w))
        for w in technical_words
    ]
    for row in rows:
        print(f"\n{row.word}")
        print(f"  word-level : {row.word_level}")
        print(f"  char-level : {len(row.char_level)} chars")
        print(f"  BPE        : {row.bpe}")
        print(f"  WordPiece  : {row.wordpiece}")

    print_section(5, "VALIDACION")
    contract_tokens = len(contrato.split())
    budgets = [
        TokenBudget(name="contrato_word_proxy", tokens=contract_tokens, attention_pairs=contract_tokens * contract_tokens),
        TokenBudget(name="contexto_duplicado", tokens=contract_tokens * 2, attention_pairs=(contract_tokens * 2) ** 2),
    ]
    for budget in budgets:
        print(f"{budget.name}: tokens={budget.tokens} pares_attention={budget.attention_pairs}")
    try:
        TokenBudget(name="mal", tokens=0, attention_pairs=0)
    except ValidationError as exc:
        print("Pydantic rechaza presupuesto sin tokens:")
        print(exc)

    print_section(6, "ANTES VS DESPUES")
    print("ANTES: word-level convierte terminos raros en [UNK].")
    print("DESPUES: subwords preservan informacion y permiten manejar vocabulario tecnico con costo controlado.")

    print_section(7, "DESAFIO PARA EL ALUMNO")
    print("1. Agrega tres palabras legales y propone BPE/WordPiece.")
    print("2. Calcula cuanto sube O(N^2) al pasar de 1.000 a 4.000 tokens.")
    print("3. Discute cuando conviene chunking en vez de contexto gigante.")

    trace_text("USER", "Tokenizá términos técnicos y estima el costo de attention.")
    trace_json("EXTRACT", [
        {
            "word": row.word,
            "word_level": row.word_level,
            "char_level_count": len(row.char_level),
            "bpe": row.bpe,
            "wordpiece": row.wordpiece,
        }
        for row in rows
    ])
    trace_json("METRICS", [budget.model_dump(mode="json") for budget in budgets])


if __name__ == "__main__":
    main()
