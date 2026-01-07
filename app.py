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

# --- 1. CONFIGURAÇÃO DE TEMA DARK PERMANENTE ---
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛", layout="centered")

# Injeção de CSS para forçar o Dark Mode e as cores da marca
st.markdown("""
    <style>
    /* Fundo principal e textos */
    .stApp {
        background-color: #000000;
        color: #E0E0E0;
    }
    /* Estilização dos Botões */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #4A0404; /* Vermelho Sangue Escuro */
        color: #ffffff;
        border: 1px solid #8B0000;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #8B0000;
        border: 1px solid #FF0000;
    }
    /* Botão do WhatsApp Especial */
    div.stLinkButton > a {
        background-color: #075E54 !important;
        color: white !important;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        display: block;
        padding: 10px;
        font-weight: bold;
        border: 1px solid #128C7E;
    }
    /* Inputs de texto */
    input {
        background-color: #1A1A1A !parse !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. EXIBIÇÃO DO LOGO ---
# O código procura pelo arquivo exatamente como você nomeou no GitHub
logo_path = "LOGO2025NOME.JPG"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, use_container_width=True)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")
    st.warning(f"Aviso: Arquivo {logo_path} não encontrado no repositório.")

st.markdown("<h2 style='text-align: center; color: #8B0000;'>Estratégias de Redenção Literária</h2>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. CONFIGURAÇÕES (SECRETS) ---
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

# Função de E-mail
def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destino
        msg['Subject'] = "📜 Sua Estratégia FAMORTISCO AI"
        msg.attach(MIMEText(conteudo, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro no portal de e-mail: {e}")
        return False

# --- 4. FLUXO DE TRABALHO ---
arquivo = st.file_uploader("Suba o Manuscrito (PDF ou DOCX)", type=['pdf', 'docx'])

if arquivo and api_key:
    try:
        # Extração de texto para ambos os formatos
        if arquivo.type == "application/pdf":
            reader = PdfReader(arquivo)
            texto = "".join([p.extract_text() or "" for p in reader.pages[:10]])
        else:
            doc = Document(arquivo)
            texto = "\n".join([p.text for p in doc.paragraphs[:100]])

        if st.button("🔥 INVOCAR ESTRATÉGIA"):
            # Rota definitiva validada nos logs e no AI Studio
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            
            prompt = f"""
            Você é um mestre de marketing para literatura sombria e gótica. 
            Com base neste texto: {texto[:3500]}
            1. Crie 3 roteiros cinematográficos para Reels.
            2. Crie 1 roteiro de ASMR focado na atmosfera do livro.
            3. Escreva um e-mail de vendas visceral para sua audiência.
            """
            
            with st.spinner('Processando a essência do seu livro...'):
                response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if response.status_code == 200:
                    st.session_state['resultado'] = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("A estratégia foi gerada com sucesso.")
                else:
                    st.error(f"Erro {response.status_code}: A IA não respondeu.")

        # Exibição e Canais de Disparo
        if 'resultado' in st.session_state:
            st.markdown("### 🖋️ O Veredito")
            st.markdown(f"<div style='background-color: #121212; padding: 20px; border-radius: 10px; border: 1px solid #4A0404;'>{st.session_state['resultado']}</div>", unsafe_allow_html=True)
            
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📧 Disparo por E-mail")
                email_dest = st.text_input("E-mail do Alvo:", placeholder="exemplo@gmail.com")
                if st.button("Enviar agora"):
                    if enviar_email(email_dest, st.session_state['resultado']):
                        st.success("E-mail enviado!")

            with col2:
                st.markdown("#### 🟢 Disparo por WhatsApp")
                num_whats = st.text_input("Número do Cliente:", value=meu_zap)
                if num_whats:
                    resumo_zap = f"*🚀 FAMORTISCO AI: ESTRATÉGIA GÓTICA*\n\n{st.session_state['resultado'][:1500]}..."
                    link_zap = f"https://api.whatsapp.com/send?phone={num_whats}&text={urllib.parse.quote(resumo_zap)}"
                    st.link_button("Abrir WhatsApp", link_zap)

    except Exception as e:
        st.error(f"Erro inesperado: {e}")
