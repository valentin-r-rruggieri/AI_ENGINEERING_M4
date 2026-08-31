"""
E02 - Tokenizacion subword y costo de contexto
AEM4L4 | Fundamentos teoricos y arquitectura

Objetivo pedagogico:
    Comparar word-level, character-level, BPE y WordPiece con terminos
    tecnicos, y conectar fragmentacion con costo aproximado de attention.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
LEGAL_PATH = DATA_DIR / "contrato_legal.txt"
VOCAB = {"cat", "contrato", "pago", "monto", "plazo", "paciente", "banco", "la", "el", "de", "servicios"}


@dataclass
class TokenizationRow:
    word: str
    word_level: list[str]
    char_level: list[str]
    bpe: list[str]
    wordpiece: list[str]


def title(text: str) -> None:
    print("\n" + "=" * 78)
    print(text)
    print("=" * 78)


def section(number: int, text: str) -> None:
    print(f"\n{number}. {text}")
    print("-" * 78)


def ensure_data() -> None:
    if LEGAL_PATH.exists():
        return
    subprocess.run([sys.executable, str(DATA_DIR / "generate_data.py")], check=True)


def word_tokenize(word: str) -> list[str]:
    return [word] if word.lower() in VOCAB else ["[UNK]"]


def char_tokenize(word: str) -> list[str]:
    return list(word)


def fake_bpe(word: str) -> list[str]:
    mapping = {
        "hypercholesterolemia": ["hyper", "cholesterol", "emia"],
        "financialization": ["financial", "ization"],
        "hipercolesterolemia": ["hiper", "colesterol", "emia"],
        "responsabilidadcontractual": ["responsabilidad", "contract", "ual"],
        "microfinanciamiento": ["micro", "financ", "iamiento"],
        "electroencefalograma": ["electro", "encefalo", "grama"],
        "confidencialidad": ["confidencial", "idad"],
    }
    return mapping.get(word.lower(), [word[i : i + 5] for i in range(0, len(word), 5)])


def fake_wordpiece(word: str) -> list[str]:
    pieces = fake_bpe(word)
    return pieces[:1] + [f"##{piece}" for piece in pieces[1:]]


def attention_pairs(tokens: int) -> int:
    return tokens * tokens


def main() -> None:
    ensure_data()
    contrato = LEGAL_PATH.read_text(encoding="utf-8").strip()
    words = [
        "cat",
        "hypercholesterolemia",
        "financialization",
        "responsabilidadcontractual",
        "microfinanciamiento",
        "confidencialidad",
    ]

    title("AEM4L4 | E02 - Tokenizacion subword")

    section(1, "Contexto")
    print("Dominios como salud, finanzas y legal tienen palabras raras o compuestas.")
    print(f"Contrato legal: {LEGAL_PATH.name}, {len(contrato.split())} palabras aproximadas")

    section(2, "Comparacion de estrategias")
    rows = [
        TokenizationRow(word, word_tokenize(word), char_tokenize(word), fake_bpe(word), fake_wordpiece(word))
        for word in words
    ]
    for row in rows:
        print(f"\n{row.word}")
        print(f"  word-level : {row.word_level}")
        print(f"  char-level : {len(row.char_level)} tokens -> {row.char_level[:12]}")
        print(f"  BPE        : {row.bpe}")
        print(f"  WordPiece  : {row.wordpiece}")

    section(3, "Costo aproximado")
    for n in [10, 30, 50, 100, len(contrato.split())]:
        print(f"{n:>4} tokens -> {attention_pairs(n):>7} pares de attention")

    section(4, "Interpretacion")
    print("[UNK] pierde informacion. Character-level conserva todo pero alarga la secuencia.")
    print("Subwords balancean cobertura y costo: representan palabras nuevas con piezas conocidas.")

    section(5, "Desafio")
    print("Agrega tres terminos legales y decide si conviene token completo, BPE o WordPiece.")


if __name__ == "__main__":
    main()
