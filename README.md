# Test Inicial — Hackathon IA Generativa

App **Streamlit** para el reto inicial del hackathon. El usuario selecciona su
grupo, responde 3 preguntas de opción múltiple, y por cada respuesta correcta
se desbloquea la descarga de un archivo:

- **Pregunta 1 correcta** → `archivos/comun_p1.zip` (común a todos los grupos).
- **Pregunta 2 correcta** → `archivos/grupo{N}_p2.zip` (depende del grupo).
- **Pregunta 3 correcta** → `archivos/caso_de_negocio.pdf` (común a todos).

> Las respuestas correctas **no** se almacenan en texto plano: sólo se guarda
> el `SHA-256` del texto exacto de la opción correcta (ver `preguntas.py`).

---

## Estructura

```
.
├── app.py                  # App principal de Streamlit
├── preguntas.py            # Preguntas, opciones y hashes de respuestas
├── requirements.txt
├── .gitignore
├── README.md
├── .streamlit/config.toml  # Tema y configuración
└── archivos/               # Archivos descargables (placeholders incluidos)
    ├── comun_p1.zip
    ├── grupo1_p2.zip
    ├── grupo2_p2.zip
    ├── grupo3_p2.zip
    ├── grupo4_p2.zip
    └── caso_de_negocio.pdf
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

- `comun_p1.zip`
- `grupo1_p2.zip`, `grupo2_p2.zip`, `grupo3_p2.zip`, `grupo4_p2.zip`
- `caso_de_negocio.pdf`

Si algún archivo falta, la app muestra un `st.warning` y no se cae.

### 2) Cambiar el texto de las opciones (sobre todo Pregunta 1)

Los textos `primer/segundo/tercer` de la P1 son provisionales. Para
reemplazarlos por los valores reales:

1. Edita el texto de la opción correcta y los distractores en `preguntas.py`.
2. **Regenera el hash** de la respuesta correcta:

   ```bash
   python preguntas.py --hash "texto exacto de la respuesta correcta"
   ```

3. Pega el hash resultante en el campo `hash_correcto` de esa pregunta.

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

Pegar aquí la URL final una vez desplegada:

```
URL pública: <pendiente>
```

---

## Alternativa: Hugging Face Spaces

Si prefieres no usar GitHub privado, también puedes desplegar gratis en
[Hugging Face Spaces](https://huggingface.co/spaces) eligiendo el SDK
**Streamlit** y subiendo el mismo proyecto.
