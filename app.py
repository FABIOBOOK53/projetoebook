import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import requests

st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Upload PDF/DOCX + geração de estratégia com Gemini 2.5")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY não configurada")
    st.stop()

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:  # limita a 5 páginas para teste rápido
            t = p.extract_text()
            if t:
                texto += t + "\n"
    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:  # limita a 50 parágrafos
            texto += p.text + "\n"
    return texto.strip()

# ---------------- UPLOAD ----------------
arquivo = st.file_uploader("Envie PDF ou DOCX", type=["pdf","docx"])

if arquivo:
    texto = extrair_texto(arquivo)
    if not texto:
        st.warning("Não foi possível extrair texto do arquivo")
    else:
        st.success("Texto extraído com sucesso")

        if st.button("Gerar Estratégia"):
            with st.spinner("Chamando a IA..."):
                # URL do modelo Gemini 2.5
                modelo_funcional = "models/gemini-2.5-flash"
                url
