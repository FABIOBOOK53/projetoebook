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
            with st.spinner('Consultando a IA...'):
                # ALTERAMOS PARA gemini-pro QUE É O MODELO ESTÁVEL COMPATÍVEL
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": f"Crie 3 posts de marketing para: {texto[:3000]}"}]}]}
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        st.markdown("### 🚀 Resultado:")
                        st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Erro {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")
else:
    st.error("⚠️ Chave GOOGLE_API_KEY não encontrada nos Secrets.")
