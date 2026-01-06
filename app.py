import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    file = st.file_uploader("Suba seu PDF", type=['pdf'])
    if file:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() or "" for p in reader.pages])
        st.success("PDF pronto para análise!")
        
        if st.button("Gerar Marketing"):
            with st.spinner('IA gerando sua estratégia...'):
                # CONFIGURAÇÃO DE SUCESSO: v1 + gemini-1.5-flash
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Crie uma estratégia de marketing viral para este ebook: {texto[:4000]}"}]
                    }]
                }
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        st.markdown("### 🚀 Estratégia Gerada:")
                        resultado = response.json()
                        st.write(resultado['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Erro do Google: {response.text}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")
else:
    st.error("⚠️ Configure a chave GOOGLE_API_KEY nos Secrets.")
