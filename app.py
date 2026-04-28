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

# =========================================================
# CONFIGURAÇÕES E ESTADOS
# =========================================================
DATA_FESTA = datetime(2026, 5, 17, 13, 0)
LOCAL_FESTA = "Rua Jaques Roberto, 225 - Bairro São Marcos"
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=Rua+Jaques+Roberto+225+Sao+Marcos"
CHAVE_PIX = "31975635794"
MEU_WHATSAPP = "5531975635794"

st.set_page_config(page_title="Quintal do Micha - Oficial", page_icon="🌳", layout="centered")

if "is_admin" not in st.session_state: st.session_state["is_admin"] = False
if "show_login" not in st.session_state: st.session_state["show_login"] = False

# =========================================================
# FUNÇÃO PARA CONVERTER IMAGEM PARA BASE64
# =========================================================
def get_base64_image(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Carregamento Masterpiece
img_path = "quintal.png"
bg_style = ""
if os.path.exists(img_path):
    img_b64 = get_base64_image(img_path)
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
# DESIGN SYSTEM (MINIMALISTA TOTAL)
# =========================================================
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap" rel="stylesheet">', unsafe_allow_html=True)
if bg_style: st.markdown(bg_style, unsafe_allow_html=True)

st.markdown("""
<style>
html, body, [class*="st-"] { font-family: "Outfit", sans-serif !important; }
.stApp { background-color: #0c0f0a; color: #f8fafc; }

/* Labels em Dourado */
label[data-testid="stWidgetLabel"] p {
    color: #facc15 !important;
    font-weight: 700 !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
}

h1, h2, h3 { color: #facc15 !important; font-weight: 900 !important; text-shadow: 2px 2px 10px rgba(0,0,0,1); }

/* Cartões Slim Glass */
.manga-real-card {
    background: rgba(0,0,0,0.6); backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1); padding: 25px;
    border-radius: 20px; margin-bottom: 20px; border-left: 5px solid #facc15;
    max-width: 600px; margin-left: auto; margin-right: auto;
}

.hero-header { text-align: center; padding: 60px 20px 30px 20px; }

/* Botões Modernos */
.stButton>button {
    width: 100%; border-radius: 12px; height: 3.5em;
    background: linear-gradient(135deg, #3f6212 0%, #1a2e19 100%);
    color: #fff !important; font-weight: 900; border: 1px solid #facc15;
    transition: 0.3s; font-size: 0.9rem;
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(250,204,21,0.2); }

/* PIX Minimalista */
.pix-min-text {
    font-size: 0.85rem !important;
    color: rgba(255,255,255,0.6) !important;
    font-style: italic;
    margin-bottom: 5px;
}
.pix-key-min {
    font-size: 1rem !important;
    color: #facc15 !important;
    font-weight: 700;
    letter-spacing: 1px;
}

footer, header, #MainMenu { visibility: hidden; }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
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
        df["WhatsApp"] = df["WhatsApp"].astype(str)
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
# UI CONVIDADO
# =========================================================

def render_header():
    st.markdown(f"""
        <div class="hero-header">
            <p style="color:#facc15; font-size:1rem; font-weight:700; letter-spacing:6px; margin-bottom:5px;">NOS BRAÇOS DA BATUCADA</p>
            <h1 style="font-size:3.5rem; margin:0; line-height:1; color:#fff;">QUINTAL DO <span style="color:#facc15;">MICHA</span></h1>
            <p style="opacity:1; margin-top:15px; font-size:1.3rem; font-style:italic; color:#fff;">"É aqui que o show vai continuar..." 🥁🎸🍻</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="manga-real-card">
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:20px; text-align:center;">
                <div style="flex:1; min-width:140px;">
                    <span style="color:#facc15; font-weight:700; font-size:0.9rem; text-transform:uppercase;">📅 QUANDO</span><br>
                    <span style="font-size:2rem; font-weight:900;">17 MAIO</span><br>
                    <span style="color:#a3e635; font-weight:700; font-size:1.1rem;">DOMINGO ÀS 13:00H</span>
                </div>
                <div style="flex:1; min-width:140px; border-left:1px solid rgba(255,255,255,0.2);">
                    <span style="color:#facc15; font-weight:700; font-size:0.9rem; text-transform:uppercase;">📍 LOCALIZAÇÃO</span><br>
                    <span style="font-size:1.1rem; font-weight:700; display:block; margin-bottom:10px;">Bairro São Marcos</span>
                    <a href="{MAPS_LINK}" target="_blank" style="background:#facc15; color:#000; padding:8px 18px; border-radius:10px; text-decoration:none; font-weight:900; font-size:0.8rem; display:inline-block;">VER MAPA 🗺️</a>
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
        st.markdown('<div class="manga-real-card">', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-weight:900; color:#facc15; margin-bottom:20px; font-size:1.2rem;'>🍻 CONFIRME SUA PRESENÇA</p>", unsafe_allow_html=True)
        nome = st.text_input("Seu Nome e Sobrenome", placeholder="Ex: Arlindo Cruz")
        col1, col2 = st.columns(2)
        vai = col1.selectbox("Vai colar?", ["Sim", "Não"])
        zap = col2.text_input("WhatsApp com DDD", placeholder="31988887777")
        n = st.slider("Leva mais gente?", 0, 12, 0)
        
        acomps = []
        if n > 0 and vai == "Sim":
            for i in range(n): acomps.append(st.text_input(f"Acompanhante {i+1}", key=f"f{i}"))

        if st.button("CONFIRMAR PRESENÇA 🚀"):
            if len(nome.strip().split()) < 2: st.error("❌ Nome completo!"); return
            if normalizar(nome) in black_list: st.error("❌ Já confirmado!"); return
            salvar_confirmacao(nome, vai, n, acomps, zap)
            st.success("🎉 Confirmado!")
            st.balloons()
            m = f"Fala Michael! Confirmado no seu Quintal!\n\nConvidado: {nome}\nAcompanhantes: {len(acomps)}"
            st.link_button("🔥 AVISAR NO WHATSAPP", f"https://api.whatsapp.com/send?phone={MEU_WHATSAPP}&text={urllib.parse.quote(m)}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Brincadeira do Micha - Versão Minimalista Total
    st.markdown(f"""
        <div style="text-align:center; margin-top:30px; padding:10px;">
            <p class="pix-min-text">Tragam presentes, kkkkk se quiser fazer um pix também aceito. 😉</p>
            <span class="pix-key-min">{CHAVE_PIX}</span>
        </div>
    """, unsafe_allow_html=True)
    
    col_pix, col_ges = st.columns([1, 1])
    with col_pix:
        # Botão de cópia ultra compacto via HTML/JS
        components.html(f"""
            <div style="text-align:right;">
                <button onclick="navigator.clipboard.writeText('{CHAVE_PIX}');alert('PIX Copiado! 🎁');" 
                style="background:rgba(250,204,21,0.2); border:1px solid #facc15; color:#facc15; padding:5px 10px; border-radius:5px; cursor:pointer; font-size:10px; font-weight:900;">
                    COPIAR PIX 📋
                </button>
            </div>
        """, height=40)
    with col_ges:
        if st.button("🔐 GESTÃO", type="secondary", key="btn_gest"):
            st.session_state["show_login"] = not st.session_state["show_login"]; st.rerun()

    if st.session_state["show_login"]:
        if st.text_input("SENHA", type="password") == st.secrets["admin"]["password"]:
            st.session_state["is_admin"] = True; st.session_state["show_login"] = False; st.rerun()

# =========================================================
# ADMIN
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

def main():
    if st.session_state["is_admin"]: render_dashboard(carregar_dados())
    else: render_header(); render_form()

if __name__ == "__main__": main()
