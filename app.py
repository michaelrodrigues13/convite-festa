import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import unicodedata
import urllib.parse
import random

# =========================================================
# CONFIGURAÇÕES E ESTADOS
# =========================================================
DATA_FESTA = datetime(2026, 5, 17, 13, 0)
LOCAL_FESTA = "Rua Jaques Roberto, 225 - Bairro São Marcos"
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=Rua+Jaques+Roberto+225+Sao+Marcos"
MEU_WHATSAPP = "5531975635794"
ARQUIVO_SAMBA = "samba.mp3"

st.set_page_config(page_title="Quintal do Micha - Oficial", page_icon="🌳", layout="centered")

if "is_admin" not in st.session_state: st.session_state["is_admin"] = False
if "show_login" not in st.session_state: st.session_state["show_login"] = False
if "music_playing" not in st.session_state: st.session_state["music_playing"] = False

# =========================================================
# FUNÇÕES DE ASSETS
# =========================================================
def get_base64_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

img_path = "quintal.png"
bg_style = ""
img_b64 = get_base64_file(img_path)
if img_b64:
    bg_style = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(12, 15, 10, 0.65), rgba(12, 15, 10, 0.65)), url("data:image/png;base64,{img_b64}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center center;
    }}
    </style>
    """

# =========================================================
# DESIGN SYSTEM
# =========================================================
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap" rel="stylesheet">', unsafe_allow_html=True)
if bg_style: st.markdown(bg_style, unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');

html, body, [class*="st-"] { font-family: "Outfit", sans-serif !important; }
.stApp { background-color: #0c0f0a; color: #f8fafc; }

/* ── Animações globais ── */
@keyframes fadeInUp {
  from { opacity:0; transform:translateY(30px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes glowPulse {
  0%, 100% { text-shadow: 0 0 8px #facc15, 0 0 20px #facc15aa; }
  50%       { text-shadow: 0 0 20px #facc15, 0 0 50px #facc15cc, 0 0 80px #facc1566; }
}
@keyframes borderGlow {
  0%, 100% { border-color: rgba(250,204,21,0.4); box-shadow: 0 0 8px rgba(250,204,21,0.15); }
  50%       { border-color: rgba(250,204,21,1);   box-shadow: 0 0 30px rgba(250,204,21,0.4); }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position:  200% center; }
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes floatBadge {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-6px); }
}

/* ── Labels amarelos ── */
label[data-testid="stWidgetLabel"] p { color: #facc15 !important; font-weight: 700; }
h1, h2, h3 { color: #facc15 !important; font-weight: 900 !important; }

/* ── Card glassmorphism ── */
.manga-real-card {
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(20px) saturate(1.4);
    -webkit-backdrop-filter: blur(20px) saturate(1.4);
    border: 1px solid rgba(250,204,21,0.25);
    padding: 28px;
    border-radius: 24px;
    margin-bottom: 20px;
    border-left: 5px solid #facc15;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    animation: fadeInUp 0.7s ease both;
    transition: box-shadow 0.3s, border-color 0.3s;
}
.manga-real-card:hover {
    box-shadow: 0 8px 40px rgba(250,204,21,0.18);
    border-color: rgba(250,204,21,0.6);
}

/* ── Hero header ── */
.hero-header {
    text-align: center;
    padding: 60px 20px 30px 20px;
    animation: fadeInUp 0.6s ease both;
}

/* ── Título principal com glow pulsante ── */
.hero-title {
    font-size: clamp(2.5rem, 9vw, 3.8rem);
    font-weight: 900;
    margin: 0;
    line-height: 1.1;
    color: #fff;
    animation: glowPulse 3s ease-in-out infinite;
}
.hero-title span { color: #facc15; }

/* ── Botões com shimmer ── */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3.5em;
    background: linear-gradient(135deg, #3f6212 0%, #1a2e19 50%, #4a7c17 100%);
    background-size: 200% auto;
    color: #fff !important;
    font-weight: 900;
    font-size: 1rem;
    border: 1px solid #facc15;
    transition: background-position 0.5s, box-shadow 0.3s, transform 0.2s;
    letter-spacing: 1px;
}
.stButton>button:hover {
    background-position: right center;
    box-shadow: 0 0 20px rgba(250,204,21,0.5);
    transform: translateY(-2px);
}
.stButton>button:active { transform: translateY(0px); }

/* ── Botão primário amarelo ── */
.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #facc15 0%, #f59e0b 50%, #facc15 100%);
    background-size: 200% auto;
    color: #0c0f0a !important;
    animation: shimmer 2.5s linear infinite;
    box-shadow: 0 0 20px rgba(250,204,21,0.4);
}

/* ── Spotlight info ── */
.cooler-spotlight {
    text-align: center;
    margin-top: 40px;
    padding: 35px;
    background: rgba(250,204,21,0.08);
    border-radius: 24px;
    border: 2px solid #facc15;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    animation: borderGlow 3s ease-in-out infinite, fadeInUp 0.9s ease both;
}

/* ── Badge flutuante ── */
.float-badge {
    display: inline-block;
    animation: floatBadge 2.5s ease-in-out infinite;
}

/* ── Inputs estilizados (Touch Targets aprimorados) ── */
.stTextInput input, .stSelectbox select {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(250,204,21,0.3) !important;
    border-radius: 12px !important;
    color: #fff !important;
    padding: 14px 16px !important;
    font-size: 1.05rem !important;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.stTextInput input:focus {
    border-color: #facc15 !important;
    box-shadow: 0 0 12px rgba(250,204,21,0.3) !important;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #facc15 !important;
    box-shadow: 0 0 10px #facc15;
}

/* ── Scroll suave ── */
html { scroll-behavior: smooth; }

/* ── Avatar header ── */
.avatar-ring {
    width: clamp(100px, 25vw, 130px); height: clamp(100px, 25vw, 130px); border-radius: 50%;
    border: 3px solid #facc15;
    box-shadow: 0 0 25px rgba(250,204,21,0.35), 0 0 60px rgba(250,204,21,0.1);
    object-fit: cover; margin: 0 auto 20px; display: block;
    animation: fadeInUp 0.5s ease both;
}

/* ── Seção atrações ── */
.atracao-grid { display:flex; justify-content:center; gap:12px; flex-wrap:wrap; max-width:600px; margin:0 auto 24px; animation: fadeInUp 0.8s ease both; }
.atracao-item {
    background: rgba(0,0,0,0.5); backdrop-filter: blur(15px);
    border: 1px solid rgba(250,204,21,0.2); border-radius: 16px;
    padding: 16px 10px; text-align: center; flex: 1 1 28%; min-width: 95px; max-width: 140px;
    transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
}
.atracao-item:hover { transform: translateY(-6px); box-shadow: 0 8px 30px rgba(250,204,21,0.2); border-color: rgba(250,204,21,0.6); }
.atracao-icon { font-size: clamp(1.6rem, 5vw, 2rem); display: block; margin-bottom: 8px; }
.atracao-label { font-size: 0.75rem; font-weight: 700; color: #facc15; letter-spacing: 1px; text-transform: uppercase; }

/* ── Rodapé premium ── */
.footer-premium { text-align:center; margin-top:50px; padding:30px 20px; border-top:1px solid rgba(250,204,21,0.15); animation: fadeInUp 1s ease both; }

footer, header, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# CORE LOGIC
# =========================================================
def normalizar(t):
    return "".join(c for c in unicodedata.normalize('NFD', str(t).strip().lower()) if unicodedata.category(c) != 'Mn') if t else ""

def carregar_dados():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0).dropna(how="all")
        for c in ["Nome do Convidado", "Vai Comparecer?", "Acompanhantes", "Nomes Acompanhantes", "WhatsApp"]:
            if c not in df.columns: df[c] = ""
        df["Acompanhantes"] = pd.to_numeric(df["Acompanhantes"], errors='coerce').fillna(0).astype(int)
        return df
    except:
        return pd.DataFrame(columns=["Nome do Convidado", "Vai Comparecer?", "Acompanhantes", "Nomes Acompanhantes", "WhatsApp"])

def salvar_confirmacao(nome, vai, n, lista, zap):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = carregar_dados()
    linha = pd.DataFrame([{"Nome do Convidado": nome.strip().title(), "Vai Comparecer?": vai, "Acompanhantes": n, "Nomes Acompanhantes": ", ".join(lista).title(), "WhatsApp": zap.strip()}])
    conn.update(data=pd.concat([df, linha], ignore_index=True))

# =========================================================
# UI CONVIDADO (SMART SAMBA)
# =========================================================
def render_audio_player():
    samba_b64 = get_base64_file(ARQUIVO_SAMBA)
    
    if not st.session_state["music_playing"]:
        st.markdown('<div style="text-align:center; padding: 100px 20px;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color:#facc15; font-weight:900;'>🌳 O portão do Quintal está aberto...</h3>", unsafe_allow_html=True)
        if st.button("🔓 ENTRAR NO QUINTAL", type="primary"):
            st.session_state["music_playing"] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    else:
        if samba_b64:
            components.html(f"""
                <audio id="samba-player" loop autoplay>
                    <source src="data:audio/mp3;base64,{samba_b64}" type="audio/mpeg">
                </audio>
                <style>
                    @keyframes eqBar {{ 0%,100%{{height:4px;}} 50%{{height:18px;}} }}
                    .eq-wrap {{ display:flex; align-items:flex-end; gap:3px; height:20px; }}
                    .eq-bar {{ width:3px; background:#facc15; border-radius:2px; animation:eqBar 0.6s ease-in-out infinite; }}
                    .eq-bar:nth-child(1){{animation-delay:0s;}} .eq-bar:nth-child(2){{animation-delay:.15s;}}
                    .eq-bar:nth-child(3){{animation-delay:.3s;}} .eq-bar:nth-child(4){{animation-delay:.1s;}}
                    .eq-bar:nth-child(5){{animation-delay:.25s;}}
                </style>
                <div style="display: flex; justify-content: flex-end; align-items: center; gap: 10px; font-family: sans-serif; color: #facc15;">
                    <div id="eq-visual" class="eq-wrap"><div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div></div>
                    <span id="music-status" style="font-size: 0.8rem; font-weight: bold;">🔊 TOCANDO SAMBA</span>
                    <button id="mute-btn" onclick="toggleMute()" style="background: rgba(250, 204, 21, 0.2); border: 1px solid #facc15; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; color: #facc15; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; transition: 0.3s;">
                        🔊
                    </button>
                </div>
                <script>
                    const player = document.getElementById('samba-player');
                    const btn = document.getElementById('mute-btn');
                    const status = document.getElementById('music-status');
                    const eq = document.getElementById('eq-visual');
                    function toggleMute() {{
                        if (player.muted) {{
                            player.muted = false; btn.innerText = '🔊'; status.innerText = '🔊 TOCANDO SAMBA';
                            btn.style.background = 'rgba(250, 204, 21, 0.2)'; eq.style.display = 'flex';
                        }} else {{
                            player.muted = true; btn.innerText = '🔇'; status.innerText = '🔇 SAMBA MUTADO';
                            btn.style.background = 'rgba(255, 255, 255, 0.1)'; eq.style.display = 'none';
                        }}
                    }}
                    document.addEventListener('visibilitychange', function() {{
                        if (document.hidden) {{ player.pause(); }} 
                        else {{ if (!player.muted) {{ player.play(); }} }}
                    }});
                </script>
            """, height=60)
        return True

def render_countdown():
    """Countdown ao vivo via JS embutido"""
    target = DATA_FESTA.strftime("%Y-%m-%dT%H:%M:00")
    components.html(f"""
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@900&display=swap" rel="stylesheet">
    <div id="countdown-wrap" style="
        font-family:'Outfit',sans-serif;
        text-align: center;
        max-width: 560px;
        margin: 10px auto 30px auto;
    ">
        <p style="color:#facc15;font-weight:700;font-size:0.85rem;letter-spacing:5px;margin:0 0 16px;">⏳ FALTAM PARA O QUINTAL</p>
        <div style="display:flex;justify-content:center;gap:6px;flex-wrap:nowrap;">
            <div class="cb"><span id="cd-d" class="cn">--</span><span class="cl">DIAS</span></div>
            <div class="cb"><span id="cd-h" class="cn">--</span><span class="cl">HORAS</span></div>
            <div class="cb"><span id="cd-m" class="cn">--</span><span class="cl">MIN</span></div>
            <div class="cb"><span id="cd-s" class="cn">--</span><span class="cl">SEG</span></div>
        </div>
    </div>
    <style>
    .cb {{ display:flex;flex-direction:column;align-items:center;background:rgba(0,0,0,0.5);border:1px solid rgba(250,204,21,0.15);border-radius:14px;padding:12px 6px;min-width:55px;flex:1 1 22%;backdrop-filter:blur(10px);box-shadow:0 4px 15px rgba(0,0,0,0.4); }}
    .cn {{ font-size:clamp(1.6rem, 6vw, 2.2rem);font-weight:900;color:#fff;line-height:1; }}
    .cl {{ font-size:0.65rem;font-weight:700;color:#facc15;letter-spacing:2px;margin-top:6px; }}
    @keyframes tickPop {{ 0%{{transform:scale(1.25);color:#facc15;}} 100%{{transform:scale(1);color:#fff;}} }}
    .tick {{ animation: tickPop 0.4s ease; }}
    </style>
    <script>
    const target = new Date("{target}");
    function pad(n){{return String(n).padStart(2,'0');}}
    function tick(){{
        const now = new Date();
        const diff = target - now;
        if(diff <= 0){{
            document.getElementById('countdown-wrap').innerHTML='<p style="color:#facc15;font-size:1.5rem;font-weight:900;">🎉 É HOJE! BORA PRO QUINTAL!</p>';
            return;
        }}
        const d=Math.floor(diff/86400000);
        const h=Math.floor((diff%86400000)/3600000);
        const m=Math.floor((diff%3600000)/60000);
        const s=Math.floor((diff%60000)/1000);
        const sd=document.getElementById('cd-s');
        sd.classList.remove('tick');
        void sd.offsetWidth;
        sd.classList.add('tick');
        document.getElementById('cd-d').innerText=pad(d);
        document.getElementById('cd-h').innerText=pad(h);
        document.getElementById('cd-m').innerText=pad(m);
        sd.innerText=pad(s);
    }}
    tick(); setInterval(tick,1000);
    </script>
    """, height=180)

def render_header():
    foto_b64 = get_base64_file("foto_micha.jpeg")
    avatar_html = f'<img src="data:image/jpeg;base64,{foto_b64}" class="avatar-ring" alt="Micha">' if foto_b64 else ''
    frases = [
        "Quem não vai, fica sem história pra contar... 🍻",
        "O cavaquinho já tá afinado, só falta você! 🎸",
        "Traz a alegria que o samba é por nossa conta! 🥁",
        "O quintal tá pronto, só falta a sua presença! 🌳",
        "Bora fazer barulho que o vizinho já tá avisado! 🔊",
        "Samba, resenha e cerveja gelada! 🍺",
    ]
    frase = random.choice(frases)
    st.markdown(f"""
        <div class="hero-header">
            {avatar_html}
            <p style="color:#facc15; font-size:1rem; font-weight:700; letter-spacing:6px; margin-bottom:5px;">NOS BRAÇOS DA BATUCADA</p>
            <h1 class="hero-title">QUINTAL DO <span>MICHA</span></h1>
            <p style="opacity:1; margin-top:15px; font-size:1.3rem; font-style:italic; color:#fff;">
                <span class="float-badge">🥁</span> "É aqui que o show vai continuar..." 
                <span class="float-badge">🎸</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <p style="text-align:center; color:rgba(255,255,255,0.75); font-style:italic; font-size:1.1rem; margin-top:5px; margin-bottom: 25px; animation: fadeInUp 1s ease both;">
            "{frase}"
        </p>
    """, unsafe_allow_html=True)

    render_countdown()
    
    st.markdown(f"""
        <div class="manga-real-card" style="animation-delay:0.2s;">
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:20px; text-align:center;">
                <div style="flex:1; min-width:140px;">
                    <span style="color:#facc15; font-weight:700; font-size:0.9rem; text-transform:uppercase;">📅 QUANDO</span><br>
                    <span style="font-size:2rem; font-weight:900;">17 MAIO</span><br>
                    <span style="color:#a3e635; font-weight:700; font-size:1.1rem;">DOMINGO ÀS 13:00H</span>
                </div>
                <div style="flex:1; min-width:140px; border-left:1px solid rgba(255,255,255,0.15);">
                    <span style="color:#facc15; font-weight:700; font-size:0.9rem; text-transform:uppercase;">📍 LOCAL</span><br>
                    <span style="font-size:1.1rem; font-weight:700; display:block; margin-bottom:10px;">Bairro São Marcos</span>
                    <a href="{MAPS_LINK}" target="_blank" style="background:linear-gradient(135deg,#facc15,#f59e0b);color:#000;padding:8px 20px;border-radius:10px;text-decoration:none;font-weight:900;font-size:0.85rem;display:inline-block;box-shadow:0 0 14px rgba(250,204,21,0.4);transition:0.3s;">VER MAPA 🗺️</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_form():
    db = carregar_dados()
    black_list = set()
    for _, r in db.iterrows():
        black_list.add(normalizar(r["Nome do Convidado"]))
        for n in str(r["Nomes Acompanhantes"]).split(","):
            if n.strip(): black_list.add(normalizar(n))

    with st.container():
        st.markdown("<p style='text-align:center; font-weight:900; color:#facc15; margin-bottom:20px; font-size:1.2rem;'>🍻 CONFIRME SUA PRESENÇA</p>", unsafe_allow_html=True)
        nome = st.text_input("Seu Nome e Sobrenome", placeholder="Ex: Arlindo Cruz")
        col1, col2 = st.columns(2)
        vai = col1.selectbox("Vai colar?", ["Sim", "Não"])
        zap = col2.text_input("WhatsApp com DDD", placeholder="31988887777")
        n = st.slider("Leva mais gente?", 0, 12, 0)
        acomps = []
        if n > 0 and vai == "Sim":
            for i in range(n): acomps.append(st.text_input(f"Acompanhante {i+1}", key=f"g{i}"))
        if st.button("🚀 CONFIRMAR MINHA PRESENÇA", type="primary"):
            if len(nome.strip().split()) < 2: st.error("❌ Coloca nome e sobrenome!"); return
            if normalizar(nome) in black_list: st.error("❌ Esse nome já confirmou!"); return
            salvar_confirmacao(nome, vai, n, acomps, zap)
            # Confetti celebration
            components.html("""
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
            <script>
            (function(){
                var end = Date.now() + 2500;
                var colors = ['#facc15','#a3e635','#ffffff','#f59e0b'];
                (function frame(){
                    confetti({particleCount:3,angle:60,spread:55,origin:{x:0},colors:colors});
                    confetti({particleCount:3,angle:120,spread:55,origin:{x:1},colors:colors});
                    if(Date.now()<end) requestAnimationFrame(frame);
                })();
            })();
            </script>
            """, height=0)
            st.success("🎉 Chegou junto! Te vejo no Quintal!")
            st.balloons()
            lista_acomps = ", ".join(filter(None, acomps)) if acomps else "Nenhum"
            m = f"Fala Michael! Confirmado no seu Quintal!\n\n✅ Convidado: {nome}\n👥 Acompanhantes ({n}): {lista_acomps}"
            st.link_button("🔥 AVISAR NO WHATSAPP", f"https://api.whatsapp.com/send?phone={MEU_WHATSAPP}&text={urllib.parse.quote(m)}", use_container_width=True)

    st.markdown(f"""
        <div class="cooler-spotlight">
            <p style="font-size:1.5rem; color:#facc15; font-weight:900; margin-bottom:15px;">🍻 TRAGA MUITA ALEGRIA E SUA BEBIDA</p>
            <p style="font-size:1.1rem; color:#f8fafc; font-weight:400; margin-bottom:20px;">Para sua comodidade, se possível traga seu cooler.</p>
            <p style="font-size:1.2rem; color:#cbd5e1; font-style:italic;">Nos vemos no samba! 🥁🎸⚽</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("🔐 GESTÃO", type="secondary", key="btn_gest_smart"):
        st.session_state["show_login"] = not st.session_state["show_login"]; st.rerun()

    if st.session_state["show_login"]:
        if st.text_input("SENHA", type="password") == st.secrets["admin"]["password"]:
            st.session_state["is_admin"] = True; st.session_state["show_login"] = False; st.rerun()

# =========================================================
# ADMIN (RESTAURADO)
# =========================================================
def render_dashboard(df):
    st.markdown("<h1 style='color:#facc15;'>📊 PLACAR DO QUINTAL</h1>", unsafe_allow_html=True)
    conf = df[df["Vai Comparecer?"] == "Sim"]
    total = int(len(conf) + conf["Acompanhantes"].sum())
    m1, m2, m3 = st.columns(3)
    m1.metric("TOTAL", total)
    m2.metric("RSVPs", len(df))
    m3.metric("NÃO", len(df[df["Vai Comparecer?"] == "Não"]))
    df_edit = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    if st.button("💾 SALVAR"):
        st.connection("gsheets", type=GSheetsConnection).update(data=df_edit); st.success("✅ Salvo!")
    if st.button("🚪 SAIR"): st.session_state["is_admin"] = False; st.rerun()

def render_atracoes():
    st.markdown("""
        <div class="atracao-grid">
            <div class="atracao-item"><span class="atracao-icon">🎸</span><span class="atracao-label">Samba</span></div>
            <div class="atracao-item"><span class="atracao-icon">🍖</span><span class="atracao-label">Churrasco</span></div>
            <div class="atracao-item"><span class="atracao-icon">🍺</span><span class="atracao-label">Cerveja<br>Gelada</span></div>
        </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
        <div class="footer-premium">
            <p style="color:rgba(250,204,21,0.6); font-size:0.85rem; font-weight:700; letter-spacing:4px; margin-bottom:8px;">QUINTAL DO MICHA</p>
            <p style="color:rgba(255,255,255,0.3); font-size:0.75rem;">Feito com 🤎 para a melhor resenha de BH</p>
            <p style="color:rgba(255,255,255,0.15); font-size:0.65rem; margin-top:5px;">© 2026</p>
        </div>
    """, unsafe_allow_html=True)

def render_particles():
    components.html("""
    <div id="pbox" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;"></div>
    <style>
    .ptc{position:absolute;width:4px;height:4px;background:radial-gradient(circle,rgba(250,204,21,0.7),transparent);border-radius:50%;animation:fUp linear infinite;opacity:0;}
    @keyframes fUp{0%{transform:translateY(100vh) scale(0);opacity:0;}15%{opacity:0.5;}85%{opacity:0.5;}100%{transform:translateY(-10vh) scale(1.2);opacity:0;}}
    </style>
    <script>
    (function(){var b=document.getElementById('pbox');for(var i=0;i<12;i++){var p=document.createElement('div');p.className='ptc';p.style.left=Math.random()*100+'%';p.style.animationDuration=(10+Math.random()*15)+'s';p.style.animationDelay=(Math.random()*12)+'s';var s=(2+Math.random()*3)+'px';p.style.width=s;p.style.height=s;b.appendChild(p);}})();
    </script>
    """, height=0)

def main():
    if st.session_state["is_admin"]: render_dashboard(carregar_dados())
    else: 
        if render_audio_player():
            render_particles()
            render_header()
            render_atracoes()
            render_form()
            render_footer()

if __name__ == "__main__": main()
