# Test Inicial — Hackathon IA Generativa

> **App en producción:** <https://techchampions-test-inicial-hackathon.streamlit.app/>

App **Streamlit** para el reto inicial del hackathon. El usuario selecciona su
grupo, ingresa la **clave de acceso de 3 dígitos** asignada por el organizador,
responde 3 preguntas **escribiendo la respuesta en una caja de texto**, y por
cada respuesta correcta se desbloquea la descarga de un archivo:

- **Pregunta 1 correcta** → `archivos/caso_de_negocio.zip` (común a todos los grupos).
- **Pregunta 2 correcta** → `archivos/{N}_p2.zip` (depende del grupo: `1_p2.zip` a `4_p2.zip`).
- **Pregunta 3 correcta** → `archivos/{N}_p3.pdf` (depende del grupo: `1_p3.pdf` a `4_p3.pdf`).

> Las respuestas correctas **no** se almacenan en texto plano: sólo se guarda
> el `SHA-256` del texto **normalizado** de la respuesta correcta (ver
> `preguntas.py`). La normalización aplica `strip` + `casefold` (minúsculas
> robustas Unicode) + colapso de espacios internos a un único espacio, así que
> `"Noviembre 2025"`, `"noviembre 2025"` y `"  NOVIEMBRE  2025 "` se consideran
> equivalentes; pero `"Nov 2025"` o `"11/2025"` **no** lo son.

---

## Estructura

```
.
├── app.py                  # App principal de Streamlit
├── preguntas.py            # Preguntas, opciones y hashes de respuestas
├── grupos.py               # Claves de acceso por grupo (SHA-256)
├── requirements.txt
├── .gitignore
├── README.md
├── .streamlit/config.toml  # Tema y configuración
└── archivos/               # Archivos descargables (placeholders incluidos)
    ├── caso_de_negocio.zip
    ├── 1_p2.zip
    ├── 2_p2.zip
    ├── 3_p2.zip
    ├── 4_p2.zip
    ├── 1_p3.pdf
    ├── 2_p3.pdf
    ├── 3_p3.pdf
    └── 4_p3.pdf
```

---

## Ejecutar localmente

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

### Workaround si `pip` falla por SSL (`CERTIFICATE_VERIFY_FAILED`)

Sólo para entornos donde el certificado raíz no esté disponible (típico en
algunas redes corporativas o Python recién instalado en Windows):

```bash
pip install -r requirements.txt ^
  --trusted-host pypi.org ^
  --trusted-host files.pythonhosted.org ^
  --trusted-host pypi.python.org
```

La app abrirá en `http://localhost:8501`.

---

## Notas para el organizador

### 1) Reemplazar los archivos descargables reales

Los 6 archivos en `archivos/` son **placeholders válidos** (zips con un
`README.txt` interno y un PDF mínimo). Antes del evento, reemplázalos por los
archivos reales **manteniendo exactamente los mismos nombres**:

- `caso_de_negocio.zip` (P1, común)
- `1_p2.zip`, `2_p2.zip`, `3_p2.zip`, `4_p2.zip` (P2, uno por grupo)
- `1_p3.pdf`, `2_p3.pdf`, `3_p3.pdf`, `4_p3.pdf` (P3, uno por grupo)

Si algún archivo falta, la app muestra un `st.warning` y no se cae.

### 2) Cambiar las claves de acceso por grupo

Las claves de 3 dígitos viven en `grupos.py` también como **SHA-256** (no en
texto plano). Para rotar una clave:

1. Genera el nuevo hash con la utilidad:
   ```bash
   python grupos.py --hash "999"
   ```
2. Pega el hash resultante en el campo correspondiente del diccionario
   `_CLAVES_HASH` dentro de `grupos.py`.
3. Comunica la nueva clave al grupo correspondiente fuera del repo (Slack,
   correo, etc.). **Nunca** dejes la clave en texto plano en el código.

### 3) Cambiar el texto de una pregunta o su respuesta correcta

Cada pregunta vive en `preguntas.py` con los campos `enunciado`, `formato`
(placeholder/ayuda) y `hash_correcto` (SHA-256 del texto normalizado de la
respuesta correcta).

Para editar una respuesta:

1. Modifica el `enunciado` y/o `formato` si lo necesitas.
2. **Regenera el hash** de la respuesta correcta (la utilidad ya aplica la
   misma normalización que la app):

   ```bash
   python preguntas.py --hash "texto de la respuesta correcta"
   ```

3. Pega el hash resultante en el campo `hash_correcto` de esa pregunta.

> Como las respuestas se ingresan por caja de texto, define un `formato` claro
> (por ejemplo `"Ej.: Enero 2023"`) para que el usuario sepa cómo responder y
> reduzca errores tipográficos.

---

## Subir a GitHub (repositorio privado recomendado)

El repo ya está inicializado con un commit en `main`. Para publicarlo:

```bash
# 1. Crea el repo (privado) en https://github.com/new
#    nombre sugerido: test-inicial-hackathon

# 2. Conecta el remoto y haz push:
git remote add origin https://github.com/<tu_usuario>/test-inicial-hackathon.git
git push -u origin main
```

> **Importante**: si el repo es **público**, los archivos de `archivos/` y los
> textos de las opciones quedarían visibles. Las respuestas correctas siguen
> protegidas por hash, pero se recomienda **repo privado** para no exponer
> los descargables.

---

## Desplegar en Streamlit Community Cloud (gratis)

1. Ir a <https://share.streamlit.io> e iniciar sesión con la cuenta de GitHub.
2. **New app** → seleccionar:
   - Repositorio: `<tu_usuario>/test-inicial-hackathon`
   - Branch: `main`
   - Main file path: `app.py`
3. Si el repo es **privado**, autoriza el scope correspondiente cuando lo pida.
4. **Deploy**. La app quedará en una URL pública tipo
   `https://<tu_usuario>-test-inicial-hackathon.streamlit.app`.
5. Cada `git push` a `main` redespliega automáticamente.

URL pública desplegada:

```
https://techchampions-test-inicial-hackathon.streamlit.app/
```

Cada `git push` a `main` redespliega automáticamente.

---

## Alternativa: Hugging Face Spaces

Si prefieres no usar GitHub privado, también puedes desplegar gratis en
[Hugging Face Spaces](https://huggingface.co/spaces) eligiendo el SDK
**Streamlit** y subiendo el mismo proyecto.
