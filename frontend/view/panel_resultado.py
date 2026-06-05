import streamlit as st

VOCALES = ["a", "e", "i", "o", "u"]
NOMBRES = {"a": "Vocal A", "e": "Vocal E", "i": "Vocal I", "o": "Vocal O", "u": "Vocal U"}
CONFETTI_COLORS = ["#7c6af5", "#3ecf6e", "#f5c542", "#e05c8a", "#4fc3f7"]
CONFETTI_POSITIONS = [
    (8,0,0.0),(18,0,0.2),(30,0,0.1),(42,0,0.3),(55,0,0.05),
    (65,0,0.25),(75,0,0.15),(85,0,0.35),(12,0,0.4),(50,0,0.45),
]

def render_resultado(resultado_placeholder, chips_placeholder):
    seña = st.session_state.ultima_seña
    seña = seña.strip().lower() if seña else None
    letra = seña.upper() if seña else "—"
    nombre = NOMBRES.get(seña, "") if seña else "Captura una seña para comenzar"

    resultado_placeholder.markdown(f"""
    <div class="card-resultado">
        <div class="seña-letra">{letra}</div>
        <div class="seña-info">
            <div class="seña-nombre">{nombre}</div>
            <div class="seña-sub">Lengua de Señas Colombiana</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chips_html = '<div class="vocales-row">'
    for v in VOCALES:
        clase = "vocal-chip activa" if v == seña else "vocal-chip"
        chips_html += f'<div class="{clase}">{v.upper()}</div>'
    chips_html += '</div>'
    chips_placeholder.markdown(chips_html, unsafe_allow_html=True)

def render_anim(anim_placeholder):
    anim = st.session_state.ultima_anim
    if anim == "feliz":
        dots = ""
        for i, (left, top, delay) in enumerate(CONFETTI_POSITIONS):
            color = CONFETTI_COLORS[i % len(CONFETTI_COLORS)]
            dots += f'<div class="confetti-dot" style="left:{left}%;background:{color};animation-delay:{delay}s"></div>'
        anim_placeholder.markdown(f"""
        <div class="confetti-container">{dots}</div>
        <div class="anim-feliz">
            <div style="font-size:2.2rem">🎉</div>
            <div style="color:#3ecf6e;font-weight:600;font-size:0.95rem;margin-top:2px">¡Excelente! Seña correcta</div>
        </div>
        """, unsafe_allow_html=True)
    elif anim == "triste":
        anim_placeholder.markdown("""
        <div class="anim-triste">
            <div style="font-size:2.2rem">😕</div>
            <div style="color:#e05c8a;font-weight:600;font-size:0.95rem;margin-top:2px">Sigue intentando</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        anim_placeholder.empty()

def render_historial_stats(historial_placeholder, stats_placeholder):
    hist = st.session_state.historial
    if hist:
        chips = ""
        for i, s in enumerate(hist[-20:]):
            clase = "hist-chip ultimo" if i == len(hist[-20:]) - 1 else "hist-chip"
            chips += f'<span class="{clase}">{s.upper()}</span>'
        historial_placeholder.markdown(f'<div style="line-height:2.2">{chips}</div>', unsafe_allow_html=True)
    else:
        historial_placeholder.markdown(
            '<span style="color:#5a5a7a;font-size:0.82rem">Aún no hay señas capturadas.</span>',
            unsafe_allow_html=True
        )

    total = len(hist)
    mas = max(set(hist), key=hist.count).upper() if hist else "—"

    stats_placeholder.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px">
        <div class="stat-card"><div class="stat-num">{total}</div><div class="stat-lbl">capturas</div></div>
        <div class="stat-card"><div class="stat-num">{mas}</div><div class="stat-lbl">más detectada</div></div>
    </div>
    """, unsafe_allow_html=True)