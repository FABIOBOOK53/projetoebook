import streamlit as st
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Upload PDF/DOCX + geração de estratégia (simulação para conta Free)")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.warning("GOOGLE_API_KEY não configurada. O app usará resposta simulada.")

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:  # limita a 5 páginas
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

# ---------------- PROCESSAMENTO ----------------
if arquivo:
    texto = extrair_texto(arquivo)
    if not texto:
        st.warning("Não foi possível extrair texto do arquivo")
    else:
        st.success("Texto extraído com sucesso")

        if st.button("Gerar Estratégia"):
            with st.spinner("Processando..."):
                # ---------------- SIMULAÇÃO PARA CONTA FREE ----------------
                resultado_simulado = (
                    "=== SIMULAÇÃO DE RESULTADO ===\n\n"
                    "Resumo do seu arquivo:\n"
                    + texto[:500]
                    + "\n\nSugestão de estratégia:\n"
                    "- Use títulos chamativos\n"
                    "- Poste snippets do conteúdo nas redes sociais\n"
                    "- Incentive engajamento com perguntas aos seguidores\n"
                    "- Crie e-mails curtos e diretos promovendo o conteúdo"
                )
                st.text_area("Resultado da IA (simulado)", resultado_simulado, height=400)
