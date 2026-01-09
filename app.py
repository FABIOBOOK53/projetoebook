import streamlit as st
import sqlite3
import hashlib
import secrets
import requests
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from PyPDF2 import PdfReader
from docx import Document

# =========================
# CONFIG
# =========================
st.set_page_config("FAMORTISCO AI", "🐦‍⬛", layout="centered")

# =========================
# SECRETS
# =========================
API_KEY = st.secrets.get("GOOGLE_API_KEY")
EMAIL_USER = st.secrets.get("EMAIL_REMETENTE")
EMAIL_PASS = st.secrets.get("EMAIL_SENHA")
APP_URL = st.secrets.get("APP_URL")

# =========================
# DATABASE
# =========================
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

# =========================
# UTILS
# =========================
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

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# RESET PASSWORD
# =========================
reset = st.query_params.get("reset")
if reset:
    st.title("🔐 Redefinir Senha")
    nova = st.text_input("Nova senha", type="password")

    if st.button("Salvar nova senha"):
        cur.execute("""
        SELECT id FROM users
        WHERE reset_token=? AND reset_expira > ?
        """, (reset, datetime.utcnow().isoformat()))
        user = cur.fetchone()

        if user:
            cur.execute("""
            UPDATE users
            SET password=?, reset_token=NULL, reset_expira=NULL
            WHERE id=?
            """, (hash_senha(nova), user[0]))
            conn.commit()
            st.success("Senha atualizada. Faça login.")
        else:
            st.error("Token inválido ou expirado.")

    st.stop()

# =========================
# LOGIN / REGISTER
# =========================
if not st.session_state.user:
    st.title("🐦‍⬛ FAMORTISCO AI")

    t1, t2, t3 = st.tabs(["Login", "Criar Conta", "Esqueci a Senha"])

    with t1:
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            cur.execute("""
            SELECT id, plano, usos FROM users
            WHERE email=? AND password=?
            """, (email, hash_senha(senha)))
            u = cur.fetchone()

            if u:
                st.session_state.user = {
                    "id": u[0],
                    "plano": u[1],
                    "usos": u[2]
                }
                st.rerun()
            else:
                st.error("Credenciais inválidas")

    with t2:
        novo_email = st.text_input("Novo e-mail")
        nova_senha = st.text_input("Nova senha", type="password")

        if st.button("Criar Conta"):
            try:
                cur.execute("""
                INSERT INTO users (email, password)
                VALUES (?, ?)
                """, (novo_email, hash_senha(nova_senha)))
                conn.commit()
                st.success("Conta criada. Faça login.")
            except:
                st.error("E-mail já cadastrado")

    with t3:
        email_reset = st.text_input("Seu e-mail")

        if st.button("Enviar link de recuperação"):
            token = gerar_token()
            expira = (datetime.utcnow() + timedelta(minutes=15)).isoformat()

            cur.execute("""
            UPDATE users SET reset_token=?, reset_expira=?
            WHERE email=?
            """, (token, expira, email_reset))
            conn.commit()

            link = f"{APP_URL}?reset={token}"
            enviar_email(
                email_reset,
                "Recuperação de senha",
                f"Clique no link para redefinir sua senha:\n\n{link}"
            )
            st.success("Link enviado por e-mail.")

    st.stop()

# =========================
# USER LOGGED
# =========================
user = st.session_state.user
st.success(f"Plano atual: {user['plano'].upper()}")

# =========================
# PLANOS
# =========================
if user["plano"] == "free":
    st.info("Plano Free: 3 usos")
    if st.button("💳 Assinar Plano PRO"):
        cur.execute("""
        UPDATE users SET plano='pro', usos=0 WHERE id=?
        """, (user["id"],))
        conn.commit()
        st.success("Plano PRO ativado (simulação)")
        st.rerun()

LIMITE = 3 if user["plano"] == "free" else 50

if user["usos"] >= LIMITE:
    st.error("Limite do plano atingido.")
    st.stop()

# =========================
# CORE APP
# =========================
st.markdown("### Upload do arquivo")
arquivo = st.file_uploader("", ["pdf", "docx", "txt"])

if arquivo and st.button("🚀 Gerar Estratégia"):
    texto = ""

    if arquivo.type == "application/pdf":
        texto = "".join(
            p.extract_text() or "" for p in PdfReader(arquivo).pages[:5]
        )
    elif arquivo.type.endswith("wordprocessingml.document"):
        texto = "\n".join(
            p.text for p in Document(arquivo).paragraphs[:50]
        )
    else:
        texto = arquivo.read().decode("utf-8")

    prompt = f"Crie estratégias de marketing para o conteúdo:\n{texto[:3000]}"
    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"
    )

    r = requests.post(url, json={
        "contents": [{"parts": [{"text": prompt}]}]
    })

    if r.status_code == 200:
        resultado = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        st.info(resultado)

        cur.execute(
            "UPDATE users SET usos = usos + 1 WHERE id=?",
            (user["id"],)
        )
        conn.commit()
    else:
        st.error(f"Erro da IA: {r.status_code}")

# =========================
# LOGOUT
# =========================
st.divider()
if st.button("Sair"):
    st.session_state.user = None
    st.rerun()
