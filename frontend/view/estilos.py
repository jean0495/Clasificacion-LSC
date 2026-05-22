import streamlit as st

def cargar_estilos():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
footer { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 0.5rem; }
.stApp { background-color: #0a0a12; }
[data-testid="stSidebar"] { background-color: #0f0f14; border-right: 1px solid #1e1e2e; }
[data-testid="stSidebar"] * { color: #a0a0b8 !important; }
.titulo-app { font-size: 1.4rem; font-weight: 600; color: #f0f0f5; letter-spacing: -0.03em; line-height: 1.2; }
.subtitulo-app { font-size: 0.8rem; color: #5a5a7a; margin-top: 2px; }
.card-resultado { background: #13131f; border: 1px solid #1e1e2e; border-radius: 14px; padding: 16px 20px; display: flex; align-items: center; gap: 16px; }
.seña-letra { font-size: 4rem; font-weight: 600; color: #7c6af5; line-height: 1; font-family: 'DM Mono', monospace; min-width: 64px; text-align: center; }
.seña-info { flex: 1; }
.seña-nombre { font-size: 0.95rem; font-weight: 500; color: #d0d0e8; }
.seña-sub { font-size: 0.78rem; color: #5a5a7a; margin-top: 2px; }
.conf-label { font-size: 0.72rem; color: #5a5a7a; margin-top: 10px; margin-bottom: 3px; }
.vocales-row { display: flex; gap: 6px; margin-top: 10px; }
.vocal-chip { flex: 1; height: 38px; border-radius: 8px; background: #1a1a2a; border: 1px solid #2a2a3a; display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 500; color: #5a5a7a; }
.vocal-chip.activa { background: #2d2060; border-color: #7c6af5; color: #c4bcff; }
.hist-chip { display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 7px; background: #1a1a2a; border: 1px solid #2a2a3a; font-size: 0.95rem; font-weight: 500; color: #a0a0b8; margin: 2px; font-family: 'DM Mono', monospace; }
.hist-chip.ultimo { background: #2d2060; border-color: #7c6af5; color: #c4bcff; }
.stat-card { background: #13131f; border: 1px solid #1e1e2e; border-radius: 10px; padding: 12px 14px; }
.stat-num { font-size: 1.4rem; font-weight: 600; color: #f0f0f5; font-family: 'DM Mono', monospace; }
.stat-lbl { font-size: 0.72rem; color: #5a5a7a; margin-top: 1px; }
.badge-activo { display: inline-block; background: #0d2e1a; color: #3ecf6e; border: 1px solid #1a4d2e; border-radius: 20px; font-size: 0.7rem; padding: 3px 9px; font-weight: 500; }
.sec-label { font-size: 0.68rem; color: #5a5a7a; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
div[data-testid="stButton"] > button { background: #7c6af5; color: #fff; border: none; border-radius: 9px; font-size: 0.88rem; font-weight: 500; padding: 9px 20px; width: 100%; transition: background 0.2s; }
div[data-testid="stButton"] > button:hover { background: #6a58e0; color: #fff; border: none; }
.modelo-card { background:#1a1a2a; border-radius:10px; padding:10px 12px; border:1px solid #2a2a3a; font-size:0.8rem; margin-bottom: 8px; }
@keyframes confetti-fall { 0% { transform: translateY(-20px) rotate(0deg); opacity: 1; } 100% { transform: translateY(80px) rotate(720deg); opacity: 0; } }
@keyframes pop-in { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
.anim-feliz { text-align: center; padding: 10px 0 4px; animation: pop-in 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.confetti-container { position: relative; height: 80px; overflow: hidden; border-radius: 10px; }
.confetti-dot { position: absolute; width: 8px; height: 8px; border-radius: 2px; animation: confetti-fall 1.2s ease-in forwards; }
@keyframes shake { 0%,100% { transform: translateX(0); } 20% { transform: translateX(-6px); } 40% { transform: translateX(6px); } 60% { transform: translateX(-4px); } 80% { transform: translateX(4px); } }
.anim-triste { text-align: center; padding: 10px 0 4px; animation: shake 0.6s ease; }
</style>
""", unsafe_allow_html=True)