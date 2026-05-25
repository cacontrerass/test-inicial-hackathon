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

CSS_TIPOGRAFIA = """
<style>
:root {
    --btn-azul: #1F6FEB;
    --btn-azul-hover: #1B5FCC;
    --btn-azul-active: #1750A8;
    --input-bg: #F1F3F6;
    --input-bg-focus: #E9ECF1;
}

/* Parrafos, listas y celdas */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    font-size: 1.12rem;
    line-height: 1.6;
}

/* Titulos */
[data-testid="stMarkdownContainer"] h1 { font-size: 2.4rem; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.95rem; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1.55rem; margin-top: 0.6rem; }

/* Captions (incluye "Formato esperado") */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
small {
    font-size: 0.98rem !important;
}

/* Texto del st.title y st.subheader */
[data-testid="stHeader"] h1 { font-size: 2.4rem; }
[data-testid="stSubheader"] h2,
[data-testid="stSubheader"] h3 { font-size: 1.6rem; }

/* Caja de texto de respuesta - fondo gris claro para contraste */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] > div > div > input,
[data-baseweb="input"] input {
    background-color: var(--input-bg) !important;
    font-size: 1.15rem;
    padding: 0.6rem 0.75rem;
    color: #1A1A1A;
}
[data-testid="stTextInput"] > div > div,
[data-baseweb="input"] {
    background-color: var(--input-bg) !important;
    border-color: #D0D5DD !important;
}
[data-testid="stTextInput"] > div > div:focus-within,
[data-baseweb="input"]:focus-within {
    background-color: var(--input-bg-focus) !important;
}
[data-testid="stTextInput"] label p { font-size: 1.05rem; }

/* Botones - azul corporativo con texto blanco */
.stButton > button,
[data-testid="stDownloadButton"] > button,
[data-testid="baseButton-primary"],
[data-testid="baseButton-secondary"] {
    font-size: 1.05rem;
    padding: 0.55rem 1.2rem;
    background-color: var(--btn-azul) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--btn-azul) !important;
    font-weight: 500;
    transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
}
.stButton > button:hover,
[data-testid="stDownloadButton"] > button:hover,
[data-testid="baseButton-primary"]:hover,
[data-testid="baseButton-secondary"]:hover {
    background-color: var(--btn-azul-hover) !important;
    border-color: var(--btn-azul-hover) !important;
    color: #FFFFFF !important;
}
.stButton > button:active,
[data-testid="stDownloadButton"] > button:active,
[data-testid="baseButton-primary"]:active,
[data-testid="baseButton-secondary"]:active,
.stButton > button:focus:not(:active),
[data-testid="stDownloadButton"] > button:focus:not(:active) {
    background-color: var(--btn-azul-active) !important;
    border-color: var(--btn-azul-active) !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}
.stButton > button p,
[data-testid="stDownloadButton"] > button p {
    color: #FFFFFF !important;
}

/* Opciones del radio (Paso 0 - Grupo) */
[data-testid="stRadio"] label p { font-size: 1.1rem; }
[data-testid="stRadio"] > label p { font-size: 1.05rem; }

/* Mensajes de alerta (success/error/warning/info) */
[data-testid="stAlert"] p,
[data-testid="stAlertContainer"] p {
    font-size: 1.1rem;
    line-height: 1.5;
}

/* Barra de progreso (texto auxiliar) */
[data-testid="stProgress"] p { font-size: 1rem; }
</style>
"""


def _inyectar_css() -> None:
    st.markdown(CSS_TIPOGRAFIA, unsafe_allow_html=True)


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
    _inyectar_css()
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
