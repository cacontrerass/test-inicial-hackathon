"""Definicion de preguntas y verificacion de respuestas.

Las respuestas correctas NO se almacenan en texto plano: solo se guarda el
hash SHA-256 del texto NORMALIZADO de la respuesta correcta.

Normalizacion aplicada (tanto al almacenar como al validar):
  - strip de espacios al inicio/final.
  - casefold (minusculas robusto a Unicode).
  - colapso de espacios internos consecutivos a un solo espacio.

Esto evita falsos negativos por mayusculas/minusculas o espacios extra en la
respuesta del usuario, sin debilitar la proteccion del hash.

Para regenerar un hash (por ejemplo si el organizador cambia el texto de una
pregunta), usar:

    python preguntas.py --hash "texto exacto de la respuesta correcta"
"""

from __future__ import annotations

import argparse
import hashlib
import re
from typing import TypedDict


class Pregunta(TypedDict, total=False):
    id: str
    enunciado: str
    formato: str
    hash_correcto: str
    imagen: str
    imagen_caption: str


def normalizar(texto: str) -> str:
    """Normaliza la respuesta del usuario antes de hashearla."""
    return re.sub(r"\s+", " ", texto.strip()).casefold()


def _h(texto: str) -> str:
    """SHA-256 (hex) del texto utf-8 ya NORMALIZADO."""
    return hashlib.sha256(normalizar(texto).encode("utf-8")).hexdigest()


PREGUNTAS: list[Pregunta] = [
    {
        "id": "q1",
        "enunciado": (
            "De acuerdo con los datos de industria, ¿para los años 2024 y 2025, "
            "cuál fue el período en el que KIA reportó el Market Share más alto?"
        ),
        "formato": "Ej.: Enero 2023",
        "hash_correcto": (
            "d5f3752ec87675019634cadc1d4740168c68eace3c227115531f7c3cdc44febc"
        ),
    },
    {
        "id": "q2",
        "enunciado": (
            "Determine la posición en el ranking de industria para el modelo "
            "KIA con más ventas en el segmento híbrido en el rango:\n\n"
            "[Fecha] >= 01.01.2024 y [Fecha] < (Var)"
        ),
        "imagen": "assets/pregunta2_var.png",
        "imagen_caption": "Ejecuta este código en Python para resolver el valor de (Var).",
        "formato": "Ej.: 8",
        "hash_correcto": (
            "4fc82b26aecb47d2868c4efbe3581732a3e7cbcc6c2efb32062c08170a05eeb8"
        ),
    },
    {
        "id": "q3",
        "enunciado": (
            "Porcentaje de crecimiento marca KIA en "
            "\"YTD(30.04.2026) vs Last Year\""
        ),
        "formato": "Ej.: 12% (incluir el signo de porcentaje)",
        "hash_correcto": (
            "062368cd48903afc05a3955f2a1104928526e99fc7dc39047297ccf094b8c709"
        ),
    },
]


def get_pregunta(qid: str) -> Pregunta:
    """Obtiene una pregunta por su id; lanza KeyError si no existe."""
    for p in PREGUNTAS:
        if p["id"] == qid:
            return p
    raise KeyError(f"Pregunta no encontrada: {qid}")


def verificar(qid: str, texto_respuesta: str | None) -> bool:
    """True si la respuesta normalizada coincide (por hash) con la correcta."""
    if texto_respuesta is None or not texto_respuesta.strip():
        return False
    pregunta = get_pregunta(qid)
    return _h(texto_respuesta) == pregunta["hash_correcto"]


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Utilidad para regenerar el hash SHA-256 (normalizado) "
            "de una respuesta correcta."
        )
    )
    parser.add_argument(
        "--hash",
        dest="texto",
        required=True,
        help="Texto de la respuesta correcta a convertir a SHA-256.",
    )
    args = parser.parse_args()
    print(_h(args.texto))


if __name__ == "__main__":
    _cli()
