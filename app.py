import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

# =====================================================
# CONFIGURAÇÃO DO APP
# =====================================================
st.set_page_config(
    page_title="FAMORTISCO AI",
    layout="centered"
)

st.title("FAMORTISCO AI")
st.subheader("Análise de PDF e DOCX com IA")

# =====================================================
# CHAVE DA API (STREAMLIT SECRETS)
# =====================================================
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY não encontrada nos Secrets.")
    st.stop()

# =====================================================
# FUNÇÃO DE EXTRAÇÃO DE TEXTO
# =====================================================
def extrair_texto(arquivo):
    texto = ""

    if arquivo.type == "application/pdf":
        leitor = PdfReader(arquivo)
        for pagina in leitor.pages[:5]:
            texto += pagina.extract_text() or ""

    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        documento = Document(arquivo)
        for paragrafo in documento.paragraphs[:50]:
            texto += paragrafo.text + "\n"

    return texto.strip()

# =====================================================
# INTERFACE
# =====================================================
arquivo = st.file_uploader(
    "Selecione um arquivo",
    type=["pdf", "docx"]
)

if arquivo is not None:
    texto_extraido = extrair_texto(arquivo)

    if texto_extraido == "":
        st.warning("Não foi possível extrair texto do arquivo.")
    else:
        st.success("Texto extraído com sucesso.")

        if st.button("🚀 Gerar Estratégia com IA"):
            with st.spinner("Chamando a IA..."):
                url = (
                    "https://generativelanguage.googleapis.com/v1beta/"
                    "models/gemini-1.0-pro:generateContent"
                    "?key=" + GOOGLE_API_KEY
                )

                prompt = (
                    "Você é um especialista em marketing digital. "
                    "Crie uma estratégia de marketing clara e prática "
                    "com base no conteúdo abaixo:\n\n"
                    + texto_extraido[:3000]
                )

                payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ]
                }

                resposta = requests.post(url, json=payload)

                if resposta.status_code == 200:
                    dados = resposta.json()

                    try:
                        resultado = dados["candidates"][0]["content"]["parts"][0]["text"]
                        st.text_area(
                            "Resultado gerado pela IA",
                            resultado,
                            height=400
                        )
                    except Exception:
                        st.error("Resposta inesperada da IA.")
                        st.json(dados)

                else:
                    st.error("Erro ao chamar a IA.")
                    st.code(resposta.text)
