"""Acceso por grupo: validacion de clave numerica de 3 digitos.

Las claves NO se almacenan en texto plano. Para cada grupo se guarda el
SHA-256 del texto normalizado de la clave correcta.

Para regenerar el hash de una clave (ej. si el organizador la rota):

    python grupos.py --hash "524"
"""

from __future__ import annotations

import argparse
import hashlib

GRUPOS: list[str] = ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4"]

# SHA-256 (hex) del texto normalizado de la clave asignada a cada grupo.
_CLAVES_HASH: dict[str, str] = {
    "Grupo 1": "388c2eafe5afd475492698c0995a2daf157eb3b3be8207391d3a023c97c8c034",
    "Grupo 2": "23c657f2efda7731a3c1990b25f318fa2eb1332208f97ab9cc2a7eac70ab5a76",
    "Grupo 3": "74de057f768beb42de17ffc4b8a56100f0bed85947ecacaef111e3d3ec997950",
    "Grupo 4": "72805ff7c0f210f3aa6e66f3f208974437611c64a2393f4e7edfef47d8e140a7",
}


def _normalizar(clave: str) -> str:
    """Normaliza la clave antes de hashearla (solo trim)."""
    return clave.strip()


def _h(texto: str) -> str:
    """SHA-256 (hex) del texto ya NORMALIZADO."""
    return hashlib.sha256(_normalizar(texto).encode("utf-8")).hexdigest()


def verificar_clave(grupo: str | None, clave: str | None) -> bool:
    """True si la clave del grupo coincide con el hash almacenado."""
    if not grupo or clave is None or not clave.strip():
        return False
    esperado = _CLAVES_HASH.get(grupo)
    if esperado is None:
        return False
    return _h(clave) == esperado


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Utilidad para regenerar el hash SHA-256 (normalizado) "
            "de una clave de grupo."
        )
    )
    parser.add_argument(
        "--hash",
        dest="texto",
        required=True,
        help="Texto de la clave correcta a convertir a SHA-256.",
    )
    args = parser.parse_args()
    print(_h(args.texto))


if __name__ == "__main__":
    _cli()
