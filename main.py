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

# ── Render inicial ────────────────────────────────────────────────────────────
render_resultado(resultado_ph, chips_ph)
render_anim(anim_ph)
render_historial_stats(historial_ph, stats_ph)

# ── Loop cámara ───────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    st.error("No se pudo acceder a la cámara.")
else:
    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                time.sleep(0.1)
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.resize(frame_rgb, (640, 480))
            h, w = frame_rgb.shape[:2]
            cx, cy, box = w // 2, h // 2, 160
            cv2.rectangle(frame_rgb, (cx-box, cy-box), (cx+box, cy+box), (124, 106, 245), 2)
            cv2.putText(frame_rgb, "Centra tu mano aqui", (cx-78, cy-box-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124, 106, 245), 1)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

            if st.session_state.limpiar_pendiente:
                for key in ["historial", "ultima_seña", "ultima_anim"]:
                    st.session_state[key] = [] if key == "historial" else None
                st.session_state.limpiar_pendiente = False
                st.session_state.necesita_render = True

            if st.session_state.captura_pendiente:
                recorte = frame_rgb[cy-box:cy+box, cx-box:cx+box]
                model, clases = get_predictor()
                seña = predecir(model, clases, recorte)
                st.session_state.ultima_seña = seña
                st.session_state.historial.append(seña)
                st.session_state.ultima_anim = "feliz"
                st.session_state.captura_pendiente = False
                st.session_state.necesita_render = True

            if st.session_state.necesita_render:
                render_resultado(resultado_ph, chips_ph)
                render_anim(anim_ph)
                render_historial_stats(historial_ph, stats_ph)
                st.session_state.necesita_render = False

            time.sleep(0.03)
    finally:
        cap.release()