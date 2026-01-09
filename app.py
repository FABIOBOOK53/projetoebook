import streamlit as st
import sqlite3
import hashlib
import requests
from PyPDF2 import PdfReader
from docx import Document

# ==============================
# CONFIGURAÇÃO
# ==============================
st.set_page_config(
    page_title="FAMORTISCO AI",
    page_icon="🐦‍⬛",
    layout="centered"
)

# ==============================
# BANCO DE DADOS (SQLite)
# ==============================
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    usos INTEGER DEFAULT 0,
    plano TEXT DEFAULT 'free'
)
""")
conn.commit()

# ==============================
# FUNÇÕES DE AUTENTICAÇÃO
# ==============================
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_usuario(email, senha):
    try:
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hash_senha(senha))
        )
        conn.commit()
        return True
    except:
        return False

def autenticar(email, senha):
    cur.execute(
        "SELECT id, plano, usos FROM users WHERE email=? AND password=?",
        (email, hash_senha(senha))
    )
    return cur.fetchone()

def incrementar_uso(user_id):
    cur.execute(
        "UPDATE users SET usos = usos + 1 WHERE id=?",
        (user_id,)
    )
    conn.commit()

# ==============================
# SESSÃO
# ==============================
if "user" not in st.session_state:
    st.session_state.user = None

# ==============================
# LOGIN / CADASTRO
# ==============================
if not st.session_state.user:
    st.title("🐦‍⬛ FAMORTISCO AI")
    st.subheader("Login ou Cadastro")

    aba = st.tabs(["Login", "Criar Conta"])

    with aba[0]:
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user = autenticar(email, senha)
            if user:
                st.session_state.user = {
                    "id": user[0],
                    "plano": user[1],
                    "usos": user[2]
                }
                st.success("Login realizado")
                st.rerun()
            else:
                st.error("Credenciais inválidas")

    with aba[1]:
        novo_email = st.text_input("Novo e-mail")
        nova_senha = st.text_input("Nova senha", type="password")
        if st.button("Criar Conta"):
            if criar_usuario(novo_email, nova_senha):
                st.success("Conta criada. Faça login.")
            else:
                st.error("E-mail já existe")

    st.stop()

# ==============================
# USUÁRIO LOGADO
# ==============================
user = st.session_state.user

st.success(f"Logado como usuário ID {user['id']} | Plano: {user['plano']}")

# ==============================
# LIMITE DE USO (FREE)
# ==============================
LIMITE_FREE = 3

if user["plano"] == "free" and user["usos"] >= LIMITE_FREE:
    st.error("Limite do plano gratuito atingido.")
    st.stop()

# ==============================
# API KEY
# ==============================
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key não configurada.")
    st.stop()

# ==============================
# INTERFACE PRINCIPAL
# ==============================
st.markdown("### Upload do Ebook")
arquivo = st.file_uploader("", type=["pdf", "docx", "txt"])

if arquivo and st.button("🚀 Gerar Estratégia"):
    texto = ""

    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        texto = "".join([p.extract_text() or "" for p in reader.pages[:5]])

    elif arquivo.type.endswith("wordprocessingml.document"):
        doc = Document(arquivo)
        texto = "\n".join([p.text for p in doc.paragraphs[:50]])

    else:
        texto = arquivo.read().decode("utf-8")

    with st.spinner("Processando..."):
        prompt = f"Crie estratégias de marketing para este conteúdo:\n{texto[:3000]}"

        url = (
            "https://generativelanguage.googleapis.com/"
            f"v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
        )

        r = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        })

        if r.status_code == 200:
            resultado = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            st.info(resultado)
            incrementar_uso(user["id"])
            st.success("Uso contabilizado")
        else:
