import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("##  LSC")
        st.markdown("Aprende la Lengua de Señas Colombiana practicando con tu cámara.")
        st.markdown("---")
        st.markdown('<div class="sec-label">modelo activo</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="modelo-card">
            <div style='color:#c4bcff;font-weight:500'>model_lsc.pth</div>
            <div style='color:#5a5a7a;margin-top:3px'>5 clases · CPU · simulado</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="sec-label">vocales disponibles</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px'>
            <span style='background:#2d2060;color:#c4bcff;border:1px solid #7c6af5;border-radius:6px;padding:3px 10px;font-size:0.85rem;font-family:monospace'>A</span>
            <span style='background:#2d2060;color:#c4bcff;border:1px solid #7c6af5;border-radius:6px;padding:3px 10px;font-size:0.85rem;font-family:monospace'>E</span>
            <span style='background:#2d2060;color:#c4bcff;border:1px solid #7c6af5;border-radius:6px;padding:3px 10px;font-size:0.85rem;font-family:monospace'>I</span>
            <span style='background:#2d2060;color:#c4bcff;border:1px solid #7c6af5;border-radius:6px;padding:3px 10px;font-size:0.85rem;font-family:monospace'>O</span>
            <span style='background:#2d2060;color:#c4bcff;border:1px solid #7c6af5;border-radius:6px;padding:3px 10px;font-size:0.85rem;font-family:monospace'>U</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button(" Limpiar historial"):
            st.session_state.limpiar_pendiente = True