import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI - Final")
st.title("🧠 BoostEbook AI - Conexão Direta")

api_key = st.secrets.get("GOOGLE_API_KEY")

file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    reader = PdfReader(file)
    texto = "".join([p.extract_text() for p in reader.pages])
    st.success("✅ Texto extraído!")

    if st.button("🚀 GERAR ESTRATÉGIA"):
        # URL DIRETA DA API (Versão estável v1)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Crie uma estratégia de marketing para: {texto[:4000]}"}]}]
        }
        
        with st.spinner('Comunicando diretamente com o Google...'):
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                texto_ia = resultado['candidates'][0]['content']['parts'][0]['text']
                st.subheader("Sua Estratégia:")
                st.write(texto_ia)
                st.balloons()
            else:
                st.error(f"Erro na conexão direta: {response.status_code}")
                st.write(response.text)
