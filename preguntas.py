"""Definicion de preguntas y verificacion de respuestas.

Las respuestas correctas NO se almacenan en texto plano: solo se guarda el
hash SHA-256 del texto exacto de la opcion correcta. Para regenerar un hash
(por ejemplo si el organizador cambia el texto de la pregunta 1), usar:

    python preguntas.py --hash "texto exacto de la respuesta correcta"
"""

from __future__ import annotations

import argparse
import hashlib
from typing import TypedDict


class Pregunta(TypedDict):
    id: str
    enunciado: str
    opciones: list[str]
    hash_correcto: str


def _h(texto: str) -> str:
    """Devuelve el hash SHA-256 (hex) del texto utf-8 indicado."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


PREGUNTAS: list[Pregunta] = [
    {
        "id": "q1",
        "enunciado": (
            "En la cultura People Team, ¿cuál es el "
            "\"tercer valor -- \" & \" primer valor\" KIA - Cluster?"
        ),
        "opciones": [
            "primer _ tercer",
            "primer -- segundo",
            "tercer - primer",
            "tercer -- primer",
            "primer – tercer",
        ],
        "hash_correcto": (
            "cedce005ff18fb49dd44cd515a294d5601a88baf6556513092459bcb64d48e3f"
        ),
    },
    {
        "id": "q2",
        "enunciado": (
            "Determine la posición en el ranking de industria para el modelo "
            "KIA con más ventas en el segmento híbrido en el rango:\n\n"
            "[Fecha] >= 01.01.2024 y [Fecha] < (Var)"
        ),
        "opciones": ["4", "7", "10", "15", "3", "11", "12"],
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
        "opciones": ["45%", "34%", "57%", "144%", "55%", "24%", "27%"],
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


def verificar(qid: str, texto_opcion: str | None) -> bool:
    """True si el texto seleccionado coincide (por hash) con la respuesta correcta."""
    if texto_opcion is None:
        return False
    pregunta = get_pregunta(qid)
    return _h(texto_opcion) == pregunta["hash_correcto"]


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Utilidad para regenerar el hash SHA-256 de una respuesta."
    )
    parser.add_argument(
        "--hash",
        dest="texto",
        required=True,
        help="Texto exacto de la opcion correcta a convertir a SHA-256.",
    )
    args = parser.parse_args()
    print(_h(args.texto))


if __name__ == "__main__":
    _cli()
