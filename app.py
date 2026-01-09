import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Extração de PDF/DOCX + IA Google AI Studio")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY não configurada")
    st.stop()

# ---------------- FUNÇÃO PARA LISTAR MODELOS ----------------
def listar_modelos(api_key):
    url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            modelos = r.json().get("models", [])
            return [m["name"] for m in modelos]
        else:
            st.error("Erro ao listar modelos")
            st.code(r.text)
            return []
    except Exception as e:
        st.error(f"Erro de conexão ao listar modelos: {e}")
        return []

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:
            t = p.extract_text()
            if t:
                texto += t + "\n"
    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:
            texto += p.text + "\n"
    return t
