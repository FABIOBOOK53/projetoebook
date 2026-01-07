import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI - Resolvido")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    try:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() for p in reader.pages])
        st.success("✅ Documento carregado!")

        if st.button("🚀 GERAR ESTRATÉGIA"):
            # A URL ABAIXO É A ÚNICA QUE FUNCIONA QUANDO TUDO FALHA
            # Ela aponta para o endpoint global estável v1
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"Resuma e crie marketing para: {texto[:3500]}"}]
                }]
            }
            
            with st.spinner('Conectando ao núcleo da IA...'):
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.write(data['candidates'][0]['content']['parts'][0]['text'])
                    st.balloons()
                else:
                    st.error(f"Erro de servidor: {response.status_code}")
                    st.info("Verifique se sua chave API no Google AI Studio tem permissão para o modelo Flash.")
    except Exception as e:
        st.error(f"Erro no processamento: {e}")
