import cv2
import numpy as np
from PIL import Image
import streamlit as st

from frontend.view.estilos import cargar_estilos
from frontend.view.sidebar import render_sidebar
from frontend.view.panel_resultado import (
    render_resultado,
    render_anim,
    render_historial_stats,
)
from core.predictor import cargar_predictor, predecir

# ─────────────────────────────────────────────
# Configuración de página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LSC · Lengua de Señas Colombiana",
    page_icon="🤟",
    layout="wide",
)

cargar_estilos()
render_sidebar()

# ─────────────────────────────────────────────
# Estado inicial
# ─────────────────────────────────────────────
DEFAULTS = {
    "historial": [],
    "ultima_seña": None,
    "ultima_anim": None,
    "limpiar_pendiente": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.limpiar_pendiente:
    st.session_state.historial = []
    st.session_state.ultima_seña = None
    st.session_state.ultima_anim = None
    st.session_state.limpiar_pendiente = False

# ─────────────────────────────────────────────
# Modelo
# ─────────────────────────────────────────────
@st.cache_resource
def get_predictor():
    return cargar_predictor()

model, clases = get_predictor()

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
c1, c2 = st.columns([5, 1])
with c1:
    st.markdown('<div class="titulo-app">Reconocimiento de señas</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-app">Lengua de Señas Colombiana · Vocales A E I O U</div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        '<div style="padding-top:6px;text-align:right">'
        '<span class="badge-activo">● en vivo</span>'
        '</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# Layout principal
# ─────────────────────────────────────────────
col_cam, col_der = st.columns([1.4, 1], gap="medium")

with col_cam:
    st.markdown('<div class="sec-label">cámara en vivo</div>', unsafe_allow_html=True)

    # ── st.camera_input: maneja todo el ciclo de vida de la cámara nativamente ──
    # Cada vez que el usuario toma una foto, este widget devuelve el frame como
    # UploadedFile (JPEG). No hay reruns artificiales ni hilos: el navegador
    # gestiona el stream y solo envía datos cuando el usuario pulsa el botón.
    foto = st.camera_input(
        label="Centra tu mano en el recuadro y pulsa el botón",
        label_visibility="collapsed",
    )

    # Overlay de instrucción debajo del widget
    st.markdown(
        '<p style="text-align:center;color:#5a5a7a;font-size:0.78rem;margin-top:4px">'
        '📷 Centra tu mano y pulsa el ícono de captura</p>',
        unsafe_allow_html=True,
    )

with col_der:
    resultado_ph  = st.empty()
    chips_ph      = st.empty()
    anim_ph       = st.empty()
    historial_ph  = st.empty()
    stats_ph      = st.empty()

# ─────────────────────────────────────────────
# Inferencia cuando hay foto nueva
# ─────────────────────────────────────────────
if foto is not None:
    # Decodificar JPEG → numpy RGB
    file_bytes = np.frombuffer(foto.getvalue(), dtype=np.uint8)
    image_bgr  = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb  = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    h, w = image_rgb.shape[:2]
    cx, cy, box = w // 2, h // 2, min(160, h // 2 - 1, w // 2 - 1)
    recorte = image_rgb[cy - box: cy + box, cx - box: cx + box]

    if recorte.size == 0:
        st.error("El recorte quedó vacío. Intenta acercar más tu mano.")
    else:
        try:
            seña = predecir(model, clases, recorte)
            st.session_state.ultima_seña  = seña
            st.session_state.ultima_anim  = "feliz"
            st.session_state.historial.append(seña)
            st.success(f"✅ Predicción: **{seña.upper()}**")
        except Exception as e:
            st.error(f"Error en la inferencia: {e}")

# ─────────────────────────────────────────────
# Render panel derecho
# ─────────────────────────────────────────────
render_resultado(resultado_ph, chips_ph)
render_anim(anim_ph)
render_historial_stats(historial_ph, stats_ph)