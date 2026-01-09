import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
from PIL import Image
import os
import mimetypes

# ==============================
# 1. CONFIGURAÇÃO DE TEMA
# ==============================
st.set_page_config(
    page_title="FAMORTISCO AI",
    page_icon="🐦‍⬛",
    layout="centered"
)

st.markdown("""
<style>
.stApp { background-color: #FFFDD0; color: #1A1A1A; }
h1, h2, h3, p, span, label { color: #1A1A1A !important; }
.stButton>button {
    width: 100%;
    border-radius: 8px;
    background-color: #0047AB;
    color: white !important;
    font-weight: bold;
    padding: 12px;
    border: none;
}
.stButton>button:hover { background-color: #2E7D32 !important; }
div.stLinkButton > a {
    background-color: #25D366 !important;
    color: white !important;
    border-radius: 8px;
    text-align: center;
    display: block;
    padding: 12px;
    font-weight: bold;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 2. LOGO
# ==============================
logo_nome = "LOGO2025NOME.jpg"
if os.path.exists(logo_nome):
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image(Image.open(logo_nome), width=250)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")

# ==============================
# 3. SECRETS
# ==============================
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

# ==============================
# 4. FUNÇÃO EMAIL
# ==============================
def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = destino
        msg["Subject"] = "📜 Estratégia Gerada - FAMORTISCO AI"
        msg.attach(MIMEText(conteudo, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

# ==============================
# 5. UPLOAD UNIVERSAL
# ==============================
st.markdown("### Procurar Arquivos")
arquivo = st.file_uploader(
    "",
    type=[
        "pdf", "docx", "txt",
        "png", "jpg", "jpeg",
        "mp4", "avi", "mov",
        "mp3", "wav"
    ],
    label_visibility="collapsed"
)

# ==============================
# 6. PROCESSAMENTO
# ==============================
if arquivo and api_key:
    try:
        mime, _ = mimetypes.guess_type(arquivo.name)
        texto_ext = None

        # ---- TEXTO ----
        if arquivo.type == "application/pdf":
            reader = PdfReader(arquivo)
            texto_ext = "".join([p.extract_text() or "" for p in reader.pages[:10]])

        elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(arquivo)
            texto_ext = "\n".join([p.text for p in doc.paragraphs[:100]])

        elif arquivo.type == "text/plain":
            texto_ext = arquivo.read().decode("utf-8")

        # ---- PRÉ-VISUALIZAÇÃO ----
        if mime:
            if mime.startswith("image"):
                st.image(arquivo)
            elif mime.startswith("video"):
                st.video(arquivo)
            elif mime.startswith("audio"):
                st.audio(arquivo)

        # ---- BOTÃO ÚNICO ----
        if st.button("🚀 GERAR MINHA ESTRATÉGIA"):
            with st.spinner("Analisando conteúdo..."):

                if texto_ext:
                    prompt = f"""
Aja como estrategista literário e de marketing.
Crie:
- Roteiros de Reels
- Conteúdo ASMR
- Copy emocional
- E-mail de vendas

Baseado neste conteúdo:
{texto_ext[:3500]}
"""
                else:
                    prompt = f"""
Recebi um arquivo de mídia.

Nome: {arquivo.name}
Tipo: {mime}

Crie ideias de marketing, roteiros, copy emocional
e estratégias comerciais adequadas a esse tipo de mídia.
"""

                url = (
                    "https://generativelanguage.googleapis.com/"
                    f"v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
                )

                resp = requests.post(url, json={
                    "contents": [{"parts": [{"text": prompt}]}]
                })

                if resp.status_code == 200:
                    st.session_state["resultado"] = (
                        resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                    )
                    st.success("Estratégia gerada com sucesso.")

        # ---- RESULTADO ----
        if "resultado" in st.session_state:
            st.info(st.session_state["resultado"])
            st.divider()

            c1, c2 = st.columns(2)

            with c1:
                dest = st.text_input("E-mail para envio:")
                if st.button("Disparar E-mail"):
                    if enviar_email(dest, st.session_state["resultado"]):
                        st.success("E-mail enviado!")

            with c2:
                num = st.text_input("WhatsApp (DDD):", value=meu_zap)
                if num:
                    resumo = f"*🐦‍⬛ FAMORTISCO AI*\n\n{st.session_state['resultado'][:1000]}"
                    link = (
                        "https://api.whatsapp.com/send?"
                        f"phone={num}&text={urllib.parse.quote(resumo)}"
                    )
                    st.link_button("Abrir WhatsApp", link)

    except Exception as e:
        st.error(f"Erro técnico: {e}")

elif not api_key:
    st.warning("Chave GOOGLE_API_KEY não encontrada nos Secrets.")
