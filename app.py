import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛")

st.title("🐦‍⬛ FAMORTISCO AI")
st.write("Versão de TESTE estável")

api_key = st.secrets.get("GOOGLE_API_KEY", "")

def extrair_texto(arquivo):
    if arquivo is None:
        return ""

    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        texto = ""
        for p in reader.pages[:5]:
            texto += p.extract_text() or ""
        return texto

    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        return "\n".join(p.text for p in doc.paragraphs[:50])

    return ""

arquivo = st.file_uploader(
    "Envie um arquivo PDF ou DOCX",
    type=["pdf", "docx"]
)

if arquivo:
    texto = extrair_texto(arquivo)

    if st.button("🚀 Gerar Estratégia"):
        if not api_key:
            st.error("API KEY não configurada")
        else:
            with st.spinner("Processando com IA..."):
                url = (
                    "https://generativelanguage.googleapis.com/v1/"
                    "models/gemini-1.5-flash:generateContent"
                    f"?key={api_key}"
                )

                prompt = (
                    "Crie uma estratégia de marketing para o seguinte conteúdo:\n\n"
                    + texto[:3000]
                )

                resp = requests.post(
                    url,
                    json={
                        "contents": [
                            {
                                "parts": [
                                    {"text": prompt}
                                ]
                            }
                        ]
                    }
                )

                if resp.status_code == 200:
                    resultado = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                    st.text_area("Resultado", resultado, height=300)
                else:
                    st.error("Erro ao chamar a IA")
