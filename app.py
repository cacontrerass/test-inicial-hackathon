"""Test Inicial - Hackathon IA Generativa.

App Streamlit: el usuario elige su grupo, responde 3 preguntas y desbloquea
un archivo por cada respuesta correcta (zip comun, zip por grupo, PDF comun).
"""

from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

from grupos import GRUPOS, descifrar_claves, verificar_clave
from preguntas import PREGUNTA_HACK, PREGUNTAS, verificar, verificar_hack

BASE_DIR = Path(__file__).parent
ARCHIVOS_DIR = BASE_DIR / "archivos"
LOGO_TECH_CHAMPIONS = BASE_DIR / "Iconos_logos" / "Logo Tech Champions - LETRAS NEGRAS.png"

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

/* Botones - azul corporativo con texto blanco.
   Se usa combinador descendiente (no `>`) porque `help="..."` envuelve
   el <button> en un tooltip extra que rompia el selector hijo directo. */
.stButton button,
[data-testid="stButton"] button,
[data-testid="stDownloadButton"] button,
[data-testid="baseButton-primary"],
[data-testid="baseButton-secondary"],
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-secondary"],
button[kind="primary"],
button[kind="secondary"] {
    font-size: 1.05rem;
    padding: 0.55rem 1.2rem;
    background-color: var(--btn-azul) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--btn-azul) !important;
    font-weight: 500;
    transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
}
.stButton button:hover,
[data-testid="stButton"] button:hover,
[data-testid="stDownloadButton"] button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover {
    background-color: var(--btn-azul-hover) !important;
    border-color: var(--btn-azul-hover) !important;
    color: #FFFFFF !important;
}
.stButton button:active,
[data-testid="stButton"] button:active,
[data-testid="stDownloadButton"] button:active,
button[kind="primary"]:active,
button[kind="secondary"]:active,
.stButton button:focus:not(:active),
[data-testid="stDownloadButton"] button:focus:not(:active) {
    background-color: var(--btn-azul-active) !important;
    border-color: var(--btn-azul-active) !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}
.stButton button p,
[data-testid="stButton"] button p,
[data-testid="stDownloadButton"] button p {
    color: #FFFFFF !important;
}

/* Boton "Hack[Descubrir contraseñas]" - estilo gris.
   Streamlit 1.36+ inyecta la clase .st-key-<key> en el contenedor
   del widget cuando se pasa el parametro key. Sobrescribe los azules
   por ser mas especifico y aparecer despues en el bloque. */
.st-key-btn_hack button,
.st-key-btn_hack [data-testid="stButton"] button,
div.st-key-btn_hack button[kind="primary"],
div.st-key-btn_hack button[kind="secondary"] {
    background-color: #B5B5B5 !important;
    color: #3F3F3F !important;
    border-color: #B5B5B5 !important;
    font-weight: 700 !important;
}
.st-key-btn_hack button p,
.st-key-btn_hack [data-testid="stButton"] button p {
    font-weight: 700 !important;
}
.st-key-btn_hack button:hover,
.st-key-btn_hack [data-testid="stButton"] button:hover {
    background-color: #9C9C9C !important;
    border-color: #9C9C9C !important;
    color: #1F1F1F !important;
}
.st-key-btn_hack button:active,
.st-key-btn_hack button:focus:not(:active) {
    background-color: #828282 !important;
    border-color: #828282 !important;
    color: #1F1F1F !important;
}
.st-key-btn_hack button p {
    color: inherit !important;
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

/* Subtitulo "Hackathon IA Generativa" - mas grande, azul, justo bajo el titulo */
[data-testid="stMarkdownContainer"] p.subtitulo-hackathon {
    color: var(--btn-azul) !important;
    font-size: 1.45rem !important;
    font-weight: 600;
    margin-top: 0.1rem !important;
    margin-bottom: 0 !important;
    line-height: 1.3;
}

/* Hipervinculos clasicos en azul Office (Power BI / SharePoint look) */
[data-testid="stMarkdownContainer"] a,
[data-testid="stMarkdownContainer"] a:link,
[data-testid="stMarkdownContainer"] a:visited {
    color: #0563C1 !important;
    text-decoration: underline;
    font-weight: 500;
}
[data-testid="stMarkdownContainer"] a:hover {
    color: #0349A0 !important;
    text-decoration: underline;
}
</style>
"""


def _inyectar_css() -> None:
    st.markdown(CSS_TIPOGRAFIA, unsafe_allow_html=True)


def _archivo_para(qid: str, grupo: str | None) -> tuple[Path, str, str]:
    """Devuelve (ruta, nombre_descarga, mime) del archivo a entregar."""
    if qid == "q1":
        return (
            ARCHIVOS_DIR / "caso_de_negocio.zip",
            "caso_de_negocio.zip",
            "application/zip",
        )
    if qid == "q2":
        n = re.search(r"\d+", grupo or "").group(0) if grupo else "1"
        nombre = f"{n}_p2.zip"
        return ARCHIVOS_DIR / nombre, nombre, "application/zip"
    if qid == "q3":
        n = re.search(r"\d+", grupo or "").group(0) if grupo else "1"
        nombre = f"{n}_p3.pdf"
        return ARCHIVOS_DIR / nombre, nombre, "application/pdf"
    raise ValueError(f"qid desconocido: {qid}")


def _init_state() -> None:
    st.session_state.setdefault("grupo", None)
    st.session_state.setdefault("grupo_confirmado", False)
    st.session_state.setdefault("ok", {"q1": False, "q2": False, "q3": False})
    st.session_state.setdefault("hack_revealed", False)
    st.session_state.setdefault("hack_ok", False)


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


def _render_hack() -> None:
    """Boton + ejercicio Hack para revelar claves de los demas grupos."""
    st.markdown("### 🛠️ Bonus")
    if st.button(
        "Hack[Descubrir contraseñas]",
        key="btn_hack",
        help="Ejercicio adicional para obtener las claves de los demas grupos.",
    ):
        st.session_state.hack_revealed = True

    if not st.session_state.hack_revealed:
        return

    st.markdown("---")
    st.info(
        "*Si resuelves el siguiente ejercicio, obtendrás las contraseñas "
        "de los demás equipos. Con esto podrás descargar todos los "
        "archivos del modelo de datos.*"
    )

    st.markdown("#### Hack")
    st.markdown(PREGUNTA_HACK["enunciado"])

    formato = PREGUNTA_HACK.get("formato", "")
    if formato:
        st.caption(f"Formato esperado · {formato}")

    respuesta = st.text_input(
        "Tu respuesta (Hack)",
        value="",
        placeholder=formato or "Escribe tu respuesta",
        key="input_qhack",
        label_visibility="collapsed",
    )

    col1, _ = st.columns([1, 3])
    with col1:
        validar = st.button("Validar respuesta", key="btn_qhack")

    if validar:
        if not respuesta or not respuesta.strip():
            st.warning("Escribe una respuesta antes de validar.")
        elif verificar_hack(respuesta):
            st.session_state.hack_ok = True
            st.success("✅ ¡Hack resuelto! Aquí están las claves de los demás grupos.")
        else:
            st.session_state.hack_ok = False
            st.error("❌ Respuesta incorrecta. Inténtalo de nuevo.")

    if st.session_state.hack_ok:
        claves = descifrar_claves()
        st.markdown("#### 🔓 Claves reveladas")
        for grupo, clave in claves.items():
            st.markdown(f"- **{grupo}** → `{clave}`")
        st.caption(
            "Usa el botón **Cambiar grupo** arriba para reingresar con la "
            "clave de otro grupo y descargar sus archivos."
        )


def _reiniciar_progreso() -> None:
    st.session_state.grupo = None
    st.session_state.grupo_confirmado = False
    st.session_state.ok = {"q1": False, "q2": False, "q3": False}
    st.session_state.hack_revealed = False
    st.session_state.hack_ok = False
    for qid in ("q1", "q2", "q3"):
        st.session_state.pop(f"input_{qid}", None)
    st.session_state.pop("input_clave", None)
    st.session_state.pop("radio_grupo", None)
    st.session_state.pop("input_qhack", None)


def main() -> None:
    st.set_page_config(
        page_title="Test Inicial — Hackathon IA Generativa",
        page_icon="🔓",
        layout="centered",
    )
    _inyectar_css()
    _init_state()

    col_titulo, col_logo = st.columns([3, 2], vertical_alignment="center")
    with col_titulo:
        st.title("🔓 Test Inicial")
        st.markdown(
            '<p class="subtitulo-hackathon">Hackathon IA Generativa</p>',
            unsafe_allow_html=True,
        )
    with col_logo:
        if LOGO_TECH_CHAMPIONS.exists():
            st.image(str(LOGO_TECH_CHAMPIONS), use_container_width=True)
    st.divider()

    if not st.session_state.grupo_confirmado:
        st.subheader("Paso 0 · Selecciona tu grupo e ingresa tu clave")
        grupo = st.radio(
            "Grupo:",
            options=GRUPOS,
            index=None,
            key="radio_grupo",
        )
        clave = st.text_input(
            "Clave de acceso (3 dígitos):",
            value="",
            max_chars=3,
            placeholder="Ej.: 123",
            key="input_clave",
            help="Solicita la clave de tu grupo al organizador.",
        )
        confirmar = st.button("Confirmar grupo", type="primary")
        if confirmar:
            if grupo is None:
                st.warning("Selecciona un grupo antes de continuar.")
            elif not clave or not clave.strip():
                st.warning("Ingresa la clave de acceso de tu grupo.")
            elif not verificar_clave(grupo, clave):
                st.error(
                    "❌ Clave incorrecta. Verifica con el organizador "
                    "la clave asignada a tu grupo e inténtalo de nuevo."
                )
            else:
                st.session_state.grupo = grupo
                st.session_state.grupo_confirmado = True
                st.rerun()
        st.info(
            "Para avanzar al Test Inicial debes seleccionar tu grupo "
            "e ingresar la clave correcta."
        )
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
    st.markdown(
        "Para resolver esta prueba tiene las siguientes herramientas a su disposición:\n\n"
        "- [Reporte Power BI – INDUSTRIA – KIA COL.]"
        "(https://app.powerbi.com/links/oJzh9Di7rM"
        "?ctid=91fadfe0-a381-436c-a36d-59d9a69deaf6&pbi_source=linkShare)\n"
        "- [Bases de datos procesadas – INDUSTRIA COL.]"
        "(https://metrokiacol-my.sharepoint.com/:f:/g/personal/reporting_kia_com_co"
        "/IgAOWi7AhmtwS70zawU2w4IGAdXxEMwtCrmzEfHFdlv-nHA?e=JtOVrh)"
    )
    for i, pregunta in enumerate(PREGUNTAS, start=1):
        _render_pregunta(i, pregunta)
        st.divider()

    if all(st.session_state.ok.values()):
        st.balloons()
        st.success(
            "🎉 ¡Felicitaciones! Has desbloqueado los 3 archivos. "
            "Ya tienes todo lo necesario para iniciar el caso de negocio."
        )

    st.divider()
    _render_hack()


if __name__ == "__main__":
    main()
