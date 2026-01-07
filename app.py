import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Chave vinda dos Segredos
api_key = st.secrets.get("GOOGLE_API_KEY")

file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    try:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() for p in reader.pages])
        st.success("✅ Documento lido!")

        if st.button("🚀 GERAR ESTRATÉGIA"):
            # A URL que força a versão v1 (estável) e evita o erro 404 v1beta
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
            
            payload = {
                "contents": [{"parts": [{"text": f"Resuma: {texto[:3000]}"}]}]
            }
            
            with st.spinner('Acessando IA...'):
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"O Google negou o acesso (Erro {response.status_code}).")
                    st.info("Isso confirma que sua chave API precisa ser liberada no Google AI Studio.")
    except Exception as e:
        st.error(f"Erro: {e}")
