import streamlit as st
import requests
import sqlite3
import os
from PyPDF2 import PdfReader
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
from PIL import Image

# ================= CONFIG =================
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛", layout="centered")

api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    plano TEXT DEFAULT 'free',
    usos INTEGER DEFAULT 0
)
""")
conn.commit()

# ================= FUNCTIONS =================
def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = destino
        msg["Subject"] = "📜 Resultado - FAMORTISCO AI"
        msg.attach(MIMEText(conteudo, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro email: {e}")
        return False

def extrair_texto(arquivo):
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        return "".join([p.extract_text() or "" for p in reader.pages[:10]])
    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        return "\n".join([p.text for p in doc.paragraphs[:100]])
    return ""

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= UI HEADER =================
logo = "LOGO2025NOME.jpg"
if os.path.exists(logo):
    st.image(Image.open(logo), width=250)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")

# ================= LOGIN =================
if not st.session_state.user:
    st.subheader("Login ou Cadastro")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Entrar"):
            cur.execute(
                "SELECT id,email,plano,usos FROM users WHERE email=? AND password=?",
                (email, senha),
            )
            u = cur.fetchone()
            if u:
                st.session_state.user = {
                    "id": u[0],
                    "email": u[1],
                    "plano": u[2],
                    "usos": u[3],
                }
                st.rerun()
            else:
                st.error("Credenciais inválidas")

    with col2:
        if st.button("Cadastrar"):
            try:
                cur.execute(
                    "INSERT INTO users (email,password) VALUES (?,?)",
                    (email, senha),
                )
                conn.commit()
                st.success("Conta criada. Faça login.")
            except:
                st.error("Email já existe")

    st.stop()

# ================= APP =================
user = st.session_state.user
st.success(f"Logado como {user['email']} | Plano: {user['plano'].upper()}")

LIMITE = 3 if user["plano"] == "free" else 50
limite_atingido = user["usos"] >= LIMITE

if user["plano"] == "free":
    st.warning("Plano FREE: até 3 usos")
    if st.button("💳 Assinar Plano PRO (teste)"):
        cur.execute(
            "UPDATE users SET plano='pro', usos=0 WHERE id=?",
            (user["id"],),
        )
        conn.commit()
        st.session_state.user["plano"] = "pro"
        st.session_state.user["usos"] = 0
        st.success("Plano PRO ativado (modo teste)")
        st.rerun()

st.divider()

arquivo = st.file_uploader("Envie PDF ou DOCX", type=["pdf", "docx"])

if arquivo:
    texto = extrair_texto(arquivo)

    if st.button("🚀 Gerar Estratégia"):
        if limite_atingido:
            st.error("Limite do plano FREE atingido.")
        else:
            with st.spinner("Gerando com IA..."):
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                prompt = f"Crie estratégias de marketing para o seguinte conteúdo:\n\n{texto[:3500]}"
                resp = requests.post(
                    url,
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                )
                if resp.status_code == 200:
                    resultado = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                    st.session_state["resultado"] = resultado

                    cur.execute(
                        "UPDATE users SET usos=usos+1 WHERE id=?",
                        (user["id"],),
                    )
                    conn.commit()
                    st.session_state.user["usos"] += 1
                else:
                    st.error("Erro ao chamar IA")

if "resultado" in st.session_state:
    st.divider()
    st.text_area("Resultado", st.session_state["resultado"], height=300)

    col1, col2 = st.columns(2)

    with col1:
        email_dest = st.text_input("Enviar por email")
        if st.button("📧 Enviar Email"):
            enviar_email(email_dest, st.session_state["resultado"])

    with col2:
        zap = st.text_input("WhatsApp", value=meu_zap)
        if zap:
            msg = urllib.parse.quote(st.session_state["resultado"][:1000])
            link = f"https://api.whatsapp.com/send?phone={zap}&text={msg}"
            st.link_button("📲 Enviar WhatsApp", link)

st.divider()
if st.button("Sair"):
    st.session_state.user = None
    st.rerun()
