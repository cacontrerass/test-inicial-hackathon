"""Test Inicial - Hackathon IA Generativa.

App Streamlit: el usuario elige su grupo, responde 3 preguntas y desbloquea
un archivo por cada respuesta correcta (zip comun, zip por grupo, PDF comun).
"""

from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

from preguntas import PREGUNTAS, verificar

BASE_DIR = Path(__file__).parent
ARCHIVOS_DIR = BASE_DIR / "archivos"

GRUPOS = ["Grupo 1", "Grupo 2", "Grupo 3", "Grupo 4"]


def _archivo_para(qid: str, grupo: str | None) -> tuple[Path, str, str]:
    """Devuelve (ruta, nombre_descarga, mime) del archivo a entregar."""
    if qid == "q1":
        return ARCHIVOS_DIR / "comun_p1.zip", "comun_p1.zip", "application/zip"
    if qid == "q2":
        n = re.search(r"\d+", grupo or "").group(0) if grupo else "1"
        nombre = f"grupo{n}_p2.zip"
        return ARCHIVOS_DIR / nombre, nombre, "application/zip"
    if qid == "q3":
        return (
            ARCHIVOS_DIR / "caso_de_negocio.pdf",
            "caso_de_negocio.pdf",
            "application/pdf",
        )
    raise ValueError(f"qid desconocido: {qid}")


def _init_state() -> None:
    st.session_state.setdefault("grupo", None)
    st.session_state.setdefault("grupo_confirmado", False)
    st.session_state.setdefault("ok", {"q1": False, "q2": False, "q3": False})


def _render_boton_descarga(qid: str) -> None:
    ruta, nombre, mime = _archivo_para(qid, st.session_state.grupo)
    if not ruta.exists():
        st.warning(
            f"⚠️ Falta el archivo `{ruta.name}` en `archivos/`. "
            "El organizador debe colocarlo antes del evento."
        )
        return
    with ruta.open("rb") as f:
        datos = f.read()
    st.download_button(
        label=f"⬇️ Descargar {nombre}",
        data=datos,
        file_name=nombre,
        mime=mime,
        key=f"dl_{qid}",
        use_container_width=True,
    )


def _render_pregunta(idx: int, pregunta: dict) -> None:
    qid = pregunta["id"]
    st.markdown(f"### Pregunta {idx}")
    st.write(pregunta["enunciado"])

    imagen_rel = pregunta.get("imagen")
    if imagen_rel:
        imagen_path = BASE_DIR / imagen_rel
        if imagen_path.exists():
            st.image(
                str(imagen_path),
                caption=pregunta.get("imagen_caption"),
                use_container_width=True,
            )
        else:
            st.warning(f"⚠️ Falta la imagen `{imagen_rel}` en el proyecto.")

    formato = pregunta.get("formato", "")
    if formato:
        st.caption(f"Formato esperado · {formato}")

    respuesta = st.text_input(
        f"Tu respuesta (Pregunta {idx})",
        value="",
        placeholder=formato or "Escribe tu respuesta",
        key=f"input_{qid}",
        label_visibility="collapsed",
    )

    col1, _ = st.columns([1, 3])
    with col1:
        validar = st.button("Validar respuesta", key=f"btn_{qid}")

    if validar:
        if not respuesta or not respuesta.strip():
            st.warning("Escribe una respuesta antes de validar.")
        elif verificar(qid, respuesta):
            st.session_state.ok[qid] = True
            st.success("✅ ¡Respuesta correcta! Archivo desbloqueado.")
        else:
            st.session_state.ok[qid] = False
            st.error("❌ Respuesta incorrecta. Inténtalo de nuevo.")

    if st.session_state.ok.get(qid):
        _render_boton_descarga(qid)


def _reiniciar_progreso() -> None:
    st.session_state.grupo = None
    st.session_state.grupo_confirmado = False
    st.session_state.ok = {"q1": False, "q2": False, "q3": False}
    for qid in ("q1", "q2", "q3"):
        st.session_state.pop(f"input_{qid}", None)


def main() -> None:
    st.set_page_config(
        page_title="Test Inicial — Hackathon IA Generativa",
        page_icon="🔓",
        layout="centered",
    )
    _init_state()

    st.title("🔓 Test Inicial")
    st.caption("Hackathon IA Generativa")
    st.divider()

    if not st.session_state.grupo_confirmado:
        st.subheader("Paso 0 · Selecciona tu grupo")
        grupo = st.radio(
            "Grupo:",
            options=GRUPOS,
            index=None,
            key="radio_grupo",
        )
        confirmar = st.button("Confirmar grupo", type="primary")
        if confirmar:
            if grupo is None:
                st.warning("Selecciona un grupo antes de confirmar.")
            else:
                st.session_state.grupo = grupo
                st.session_state.grupo_confirmado = True
                st.rerun()
        st.info("Hasta confirmar el grupo no se mostrarán las preguntas.")
        return

    cols = st.columns([3, 1])
    with cols[0]:
        st.success(f"Grupo seleccionado: **{st.session_state.grupo}**")
    with cols[1]:
        if st.button("Cambiar grupo", help="Reinicia el progreso"):
            _reiniciar_progreso()
            st.rerun()

    resueltas = sum(1 for v in st.session_state.ok.values() if v)
    st.progress(resueltas / 3, text=f"Progreso: {resueltas}/3 preguntas correctas")

    st.divider()
    for i, pregunta in enumerate(PREGUNTAS, start=1):
        _render_pregunta(i, pregunta)
        st.divider()

    if all(st.session_state.ok.values()):
        st.balloons()
        st.success(
            "🎉 ¡Felicitaciones! Has desbloqueado los 3 archivos. "
            "Ya tienes todo lo necesario para iniciar el caso de negocio."
        )


if __name__ == "__main__":
    main()
