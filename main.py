import cv2
import numpy as np
import streamlit as st

from frontend.view.estilos import cargar_estilos
from frontend.view.sidebar import render_sidebar
from frontend.view.panel_resultado import (
    render_resultado,
    render_anim,
    render_historial_stats
)

from core.predictor import (
    cargar_predictor,
    predecir
)

# ─────────────────────────────────────────────
# Configuración página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LSC · Lengua de Señas Colombiana",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="auto",
)

cargar_estilos()
render_sidebar()

# ─────────────────────────────────────────────
# Estado
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

# limpiar historial
if st.session_state.limpiar_pendiente:
    st.session_state.historial = []
    st.session_state.ultima_seña = None
    st.session_state.ultima_anim = None
    st.session_state.limpiar_pendiente = False

# ─────────────────────────────────────────────
# Modelo en RAM
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def cargar_modelo_en_memoria():
    print("🚀 Modelo cargado en RAM")
    return cargar_predictor()

MODEL, CLASES = cargar_modelo_en_memoria()

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
c1, c2 = st.columns([5, 1])

with c1:
    st.markdown(
        '<div class="titulo-app">Reconocimiento de señas</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo-app">Lengua de Señas Colombiana · Vocales A E I O U</div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div style="padding-top:6px;text-align:right">
            <span class="badge-activo">● activo</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Layout
# ─────────────────────────────────────────────
col_cam, col_der = st.columns([1.4, 1], gap="medium")

# ======================================================
# CÁMARA
# ======================================================
with col_cam:

    st.markdown(
        '<div class="sec-label">captura de imagen</div>',
        unsafe_allow_html=True
    )

    foto = st.camera_input(
        "📸 Captura tu seña dentro del encuadre"
    )

    st.markdown(
        """
        <div style="
            color:#5a5a7a;
            font-size:0.82rem;
            text-align:center;
            padding:6px 0">
            Centra tu mano y toma una fotografía
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# PANEL DERECHO
# ======================================================
with col_der:

    st.markdown(
        '<div class="sec-label">resultado</div>',
        unsafe_allow_html=True
    )

    resultado_ph = st.empty()
    chips_ph = st.empty()

    anim_ph = st.empty()

    st.markdown(
        "<div style='margin-top:12px'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sec-label">historial de sesión</div>',
        unsafe_allow_html=True
    )

    historial_ph = st.empty()

    st.markdown(
        "<div style='margin-top:10px'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sec-label">estadísticas</div>',
        unsafe_allow_html=True
    )

    stats_ph = st.empty()

# ─────────────────────────────────────────────
# Inferencia
# ─────────────────────────────────────────────
if foto is not None:

    try:

        file_bytes = np.frombuffer(
            foto.getvalue(),
            dtype=np.uint8
        )

        image_bgr = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )

        image_rgb = cv2.cvtColor(
            image_bgr,
            cv2.COLOR_BGR2RGB
        )

        h, w = image_rgb.shape[:2]

        cx = w // 2
        cy = h // 2

        box = min(
            160,
            h // 2 - 1,
            w // 2 - 1
        )

        recorte = image_rgb[
            cy-box:cy+box,
            cx-box:cx+box
        ]

        if recorte.size > 0:

            seña = predecir(
                MODEL,
                CLASES,
                recorte
            )

            st.session_state.ultima_seña = seña
            st.session_state.ultima_anim = "feliz"
            st.session_state.historial.append(seña)

        else:
            st.error(
                "No se pudo obtener una región válida de la imagen."
            )

    except Exception as e:

        st.error(
            f"Error durante la inferencia: {e}"
        )

# ─────────────────────────────────────────────
# Render UI
# ─────────────────────────────────────────────
render_resultado(
    resultado_ph,
    chips_ph
)

render_anim(
    anim_ph
)

render_historial_stats(
    historial_ph,
    stats_ph
)