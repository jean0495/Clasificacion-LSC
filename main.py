import cv2
import time
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LSC · Lengua de Señas Colombiana",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="auto",
)

from frontend.view.estilos import cargar_estilos
from frontend.view.sidebar import render_sidebar
from frontend.view.panel_resultado import render_resultado, render_anim, render_historial_stats
from core.predictor import cargar_predictor, predecir

cargar_estilos()
render_sidebar()

# ── Estado ───────────────────────────────────────────────────────────────────
for key, val in [
    ("historial", []), ("ultima_seña", None),
    ("ultima_anim", None), ("captura_pendiente", False),
    ("limpiar_pendiente", False), ("necesita_render", False),
]:
    if key not in st.session_state:
        st.session_state[key] = val

@st.cache_resource
def get_predictor():
    return cargar_predictor()

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

    components.html("""
    <script>
        window.parent.document.addEventListener('keydown', function(e) {
            if (e.code === 'Space') {
                e.preventDefault();
                const btns = window.parent.document.querySelectorAll('button');
                btns.forEach(function(btn) {
                    if (btn.innerText.includes('Capturar')) {
                        btn.click();
                    }
                });
            }
        });
    </script>
    """, height=0)

    st.markdown('<div style="color:#5a5a7a;font-size:0.82rem;text-align:center;padding:6px 0">Presiona <kbd style="background:#1a1a2a;border:1px solid #2a2a3a;border-radius:4px;padding:2px 8px;color:#c4bcff;font-family:monospace">ESPACIO</kbd> para capturar</div>', unsafe_allow_html=True)

    if st.button("📸 Capturar seña"):
        st.session_state.captura_pendiente = True

with col_der:
    st.markdown('<div class="sec-label">resultado</div>', unsafe_allow_html=True)
    resultado_ph = st.empty()
    chips_ph     = st.empty()
    anim_ph      = st.empty()
    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">historial de sesión</div>', unsafe_allow_html=True)
    historial_ph = st.empty()
    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">estadísticas</div>', unsafe_allow_html=True)
    stats_ph     = st.empty()

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

            UMBRAL_MINIMO = 0.90
            if st.session_state.captura_pendiente:
                recorte = frame_rgb[cy-box:cy+box, cx-box:cx+box]
                model, clases = get_predictor()
                seña, conf = predecir(model, clases, recorte)

                if conf >= UMBRAL_MINIMO:
                    st.session_state.ultima_seña = seña
                    st.session_state.historial.append(seña)
                    st.session_state.ultima_anim = "feliz"
                else: 
                    st.session_state.ultima_seña = None
                    st.session_state.ultima_anim = "triste"
                  
                st.session_state.captura_pendiente = False
                st.session_state.necesita_render = True

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