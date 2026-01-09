import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

# ---------------- CONFIGURACAO ----------------
st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Analise de PDF e DOCX com Gemini")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if API_KEY is None or API_KEY == "":
    st.error("GOOGLE_API_KEY nao encontrada nos Secrets")
    st.stop()

# ---------------- FUNCAO ----------------
def extrair_texto(arquivo):
    texto = ""

    if arquivo.type == "application/pdf":
        leitor = PdfReader(arquivo)
        for pagina in leitor.pages[:5]:
            texto = texto + (pagina.extract_text() or "")

    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        documento = Document(arquivo)
        for p in documento.paragraphs[:50]:
            texto = texto + p.text + "\n"

    return texto.strip()

# ---------------- UPLOAD ----------------
arquivo = st.file_uploader("Selecione um arquivo PDF ou DOCX", type=["pdf", "docx"])

# ---------------- FLUXO ----------------
if arquivo is not None:
    texto_extraido = extrair_texto(arquivo)

    if texto_e_
