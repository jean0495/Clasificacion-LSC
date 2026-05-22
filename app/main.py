import cv2
import time
import random
import numpy as np
import streamlit as st

from componentes.estilos import cargar_estilos
from componentes.sidebar import render_sidebar
from componentes.panel_resultado import render_resultado, render_anim, render_historial_stats

st.set_page_config(
    page_title="LSC · Lengua de Señas Colombiana",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto",
)

cargar_estilos()
render_sidebar()

# ── Estado ───────────────────────────────────────────────────────────────────
for key, val in [
    ("historial", []), ("ultima_seña", None), ("ultima_conf", None),
    ("ultima_anim", None), ("captura_pendiente", False), ("limpiar_pendiente", False),
]:
    if key not in st.session_state:
        st.session_state[key] = val

UMBRAL_FELIZ = 0.95
VOCALES = ["A", "E", "I", "O", "U"]

def predecir_simulado(frame: np.ndarray) -> tuple[str, float]:
    return random.choice(VOCALES), round(random.uniform(0.70, 0.99), 2)

# ── Encabezado ───────────────────────────────────────────────────────────────
c1, c2 = st.columns([5, 1])
with c1:
    st.markdown('<div class="titulo-app">Reconocimiento de señas</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-app">Lengua de Señas Colombiana · Practica las vocales A E I O U</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div style="padding-top:6px;text-align:right"><span class="badge-activo">● en vivo</span></div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

# ── Layout ───────────────────────────────────────────────────────────────────
col_cam, col_der = st.columns([1.4, 1], gap="medium")

with col_cam:
    st.markdown('<div class="sec-label">cámara en vivo</div>', unsafe_allow_html=True)
    frame_placeholder = st.empty()
    if st.button("📸 Capturar seña"):
        st.session_state.captura_pendiente = True

with col_der:
    st.markdown('<div class="sec-label">resultado</div>', unsafe_allow_html=True)
    resultado_ph = st.empty()
    chips_ph     = st.empty()
    progreso_ph  = st.empty()
    anim_ph      = st.empty()
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">historial de sesión</div>', unsafe_allow_html=True)
    historial_ph = st.empty()
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">estadísticas</div>', unsafe_allow_html=True)
    stats_ph     = st.empty()

# ── Render inicial ────────────────────────────────────────────────────────────
render_resultado(resultado_ph, chips_ph, progreso_ph)
render_anim(anim_ph)
render_historial_stats(historial_ph, stats_ph)

# ── Loop cámara ───────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("No se pudo acceder a la cámara.")
else:
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w = frame_rgb.shape[:2]
            cx, cy, box = w // 2, h // 2, 160
            cv2.rectangle(frame_rgb, (cx-box, cy-box), (cx+box, cy+box), (124, 106, 245), 2)
            cv2.putText(frame_rgb, "Centra tu mano aqui", (cx-78, cy-box-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124, 106, 245), 1)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

            if st.session_state.limpiar_pendiente:
                for key in ["historial", "ultima_seña", "ultima_conf", "ultima_anim"]:
                    st.session_state[key] = [] if key == "historial" else None
                st.session_state.limpiar_pendiente = False
                render_resultado(resultado_ph, chips_ph, progreso_ph)
                render_anim(anim_ph)
                render_historial_stats(historial_ph, stats_ph)

            if st.session_state.captura_pendiente:
                seña, conf = predecir_simulado(frame_rgb)
                st.session_state.ultima_seña = seña
                st.session_state.ultima_conf = conf
                st.session_state.historial.append(seña)
                st.session_state.ultima_anim = "feliz" if conf >= UMBRAL_FELIZ else "triste"
                st.session_state.captura_pendiente = False
                render_resultado(resultado_ph, chips_ph, progreso_ph)
                render_anim(anim_ph)
                render_historial_stats(historial_ph, stats_ph)

            time.sleep(0.03)
    finally:
        cap.release()