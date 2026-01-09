import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Extração de PDF/DOCX + IA Gemini API")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY não configurada nos Secrets")
    st.stop()

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""

    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:
            texto += p.extract_text() or ""

    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:
            texto += p.text + "\n"

    return texto.strip()

# ---------------- UPLOAD DE ARQUIVO ----------------
arquivo = st.file_uploader("Selecione PDF ou DOCX", type=["pdf", "docx"])

if arquivo:
    texto = extrair_texto(arquivo)

    if not texto:
        st.warning("Não foi possível extrair texto do arquivo")
    else:
        st.success("Texto extraído com sucesso")

        # ---------------- BOTÃO DE AÇÃO ----------------
        if st.button("🚀 Gerar Estratégia com IA"):

            with st.spinner("Chamando a IA.
