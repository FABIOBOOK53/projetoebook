import streamlit as st
import sqlite3
import hashlib
import secrets
import requests
import smtplib
import urllib.parse
import os
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from PyPDF2 import PdfReader
from docx import Document

# ================= CONFIG =================
st.set_page_config(
    page_title="FAMORTISCO AI",
    page_icon="🐦‍⬛",
    layout="centered"
)

API_KEY = st.secrets.get("GOOGLE_API_KEY")
EMAIL_USER = st.secrets.get("EMAIL_REMETENTE")
EMAIL_PASS = st.secrets.get("EMAIL_SENHA")
MEU_ZAP = st.secrets.get("MEU_WHATSAPP", "")
APP_URL = st.secrets.get("APP_URL", "")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= DATABASE (TESTE LOCAL) =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    plano TEXT DEFAULT 'free',
    usos INTEGER DEFAULT 0,
    reset_token TEXT,
    reset_expira TEXT
)
""")
conn.commit()

# ================= UTILS =================
def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def gerar_token():
    return secrets.token_urlsafe(32)

def enviar_email(dest, assunto, corpo):
    msg = MIMEText(corpo)
    msg["From"] = EMAIL_USER
    msg["To"] = dest
    msg["Subject"] = assunto
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
    server.quit()

def enviar_email_anexo(dest, assunto, corpo, caminho):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = dest
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain"))

    with open(caminho, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{os.path.basename(caminho)}"'
    )
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
    server.quit()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None
if "resultado" not in st.session_state:
    st.session_state.resultado = None

# ================= RESET DE SENHA =================
params = st.query_params
if "reset" in params:
    st.title("🔐 Redefinir senha")
    nova = st.text_input("Nova senha", type="password")

    if st.button("Salvar nova senha"):
        cur.execute(
            "SELECT id FROM users WHERE reset_token=? AND reset_expira > ?",
            (params["reset"], datetime.utcnow().isoformat())
        )
        u = cur.fetchone()

        if u:
            cur.execute(
                "UPDATE users SET password=?, reset_token=NULL, reset_expira=NULL WHERE id=?",
                (hash_senha(nova), u[0])
            )
            conn.commit()
            st.success("Senha redefinida. Faça login.")
        else:
            st.error("Token inválido ou expirado.")
    st.stop()

# ================= LOGIN / CADASTRO =================
if not st.session_state.user:
    st.title("🐦‍⬛ FAMORTISCO AI")

    t1, t2, t3 = st.tabs(["Login", "Criar Conta", "Esqueci a Senha"])

    with t1:
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            cur.execute(
                "SELECT id, plano, usos FROM users WHERE email=? AND password=?",
                (email, hash_senha(senha))
            )
            u = cur.fetchone()
            if u:
                st.session_state.user = {
                    "id": u[0],
                    "plano": u[1],
                    "usos": u[2]
                }
                st.experimental_rerun()
            else:
                st.error("Credenciais inválidas")

    with t2:
        email = st.text_input("Novo e-mail")
        senha = st.text_input("Nova senha", type="password")
        if st.button("Criar Conta"):
            try:
                cur.execute(
                    "INSERT INTO users (email, password) VALUES (?, ?)",
                    (email, hash_senha(senha))
                )
                conn.commit()
                st.success("Conta criada com sucesso.")
            except:
                st.error("E-mail já cadastrado")

    with t3:
        email = st.text_input("Seu e-mail")
        if st.button("Enviar link"):
            tk = gerar_token()
            exp = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
            cur.execute(
                "UPDATE users SET reset_token=?, reset_expira=? WHERE email=?",
                (tk, exp, email)
            )
            conn.commit()
            enviar_email(email, "Recuperação de senha", f"{APP_URL}?reset={tk}")
            st.success("Link enviado por e-mail")

    st.stop()

# ================= USUÁRIO LOGADO =================
user = st.session_state.user
st.success(f"Plano atual: {user['plano'].upper()}")

# ================= PLANO (TESTE) =================
if user["plano"] == "free":
    st.warning("Plano FREE (até 3 usos)")
    if st.button("💳 Assinar Plano PRO"):
        cur.execute(
            "UPDATE users SET plano='pro', usos=0 WHERE id=?",
            (user["id"],)
        )
        conn.commit()

        # atualização imediata da sessão
        st.session_state.user["plano"] = "pro"
        st.session_state.user["usos"] = 0

        st.success("Plano PRO ativado (modo teste)")
        st.experimental_rerun()

# controle de limite SEM travar app
LIMITE = 3 if user["plano"] == "free" else 50
limite_atingido = user["usos"] >= LIMITE

# ================= GERAR TEXTO =================
st.markdown("## 📘 Gerar estratégia a partir de arquivo")
arquivo = st.file_uploader("Upload de PDF, DOCX ou TXT", ["pdf", "docx", "txt"])

if st.button("🚀 Gerar Estratégia"):
    if limite_atingido:
        st.warning("Limite do plano FREE atingido.")
        st.info("Assine o Plano PRO para continuar.")
    elif not arquivo:
        st.warning("Envie um arquivo primeiro.")
    else:
        texto = ""
        if arquivo.type == "application/pdf":
            texto = "".join(p.extract_text() or "" for p in PdfReader(arquivo).pages[:5])
        elif "word" in arquivo.type:
            texto = "\n".join(p.text for p in Document(arquivo).paragraphs[:50])
        else:
            texto = arquivo.read().decode("utf-8")

        prompt = f"Crie uma estratégia de marketing para:\n{texto[:3000]}"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"

        r = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        })

        if r.status_code == 200:
            st.session_state.resultado = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            cur.execute("UPDATE users SET usos = usos + 1 WHERE id=?", (user["id"],))
            conn.commit()
        else:
            st.error("Erro ao gerar conteúdo.")

# ================= RESULTADO =================
if st.session_state.resultado:
    st.info(st.session_state.resultado)

    email_envio = st.text_input("Enviar resultado por e-mail")
    if st.button("📧 Enviar Resultado"):
        enviar_email(
            email_envio,
            "Resultado FAMORTISCO AI",
            st.session_state.resultado
        )
        st.success("Resultado enviado por e-mail")

    zap_link = f"https://api.whatsapp.com/send?phone={MEU_ZAP}&text={urllib.parse.quote(st.session_state.resultado[:800])}"
    st.link_button("📲 Enviar no WhatsApp", zap_link)

# ================= UPLOAD DE ARQUIVO PRONTO =================
st.divider()
st.markdown("## 📎 Enviar arquivo pronto")

midia = st.file_uploader(
    "PDF, DOC, DOCX, AVI, MP3 ou WAV",
    ["pdf", "doc", "docx", "avi", "mp3", "wav"]
)

if midia:
    caminho = os.path.join(UPLOAD_DIR, midia.name)
    with open(caminho, "wb") as f:
        f.write(midia.getbuffer())
    st.success("Arquivo carregado")

    email_arq = st.text_input("Enviar arquivo por e-mail")
    if st.button("📧 Enviar Arquivo"):
        enviar_email_anexo(
            email_arq,
            "Arquivo enviado pelo FAMORTISCO AI",
            "Segue o arquivo conforme solicitado.",
            caminho
        )
        st.success("Arquivo enviado por e-mail")

    link = f"{APP_URL}/{UPLOAD_DIR}/{midia.name}"
    zap = f"https://api.whatsapp.com/send?phone={MEU_ZAP}&text={urllib.parse.quote(link)}"
    st.link_button("📲 Enviar link no WhatsApp", zap)

# ================= LOGOUT =================
st.divider()
if st.button("Sair"):
    st.session_state.clear()
    st.experimental_rerun()
