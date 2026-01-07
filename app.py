import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI - Final", layout="centered")
st.title("🧠 BoostEbook AI")

# Chave vinda dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    try:
        reader = PdfReader(file)
        # Lemos apenas 3 páginas para não estourar o limite da chave Free
        texto = "".join([p.extract_text() or "" for p in reader.pages[:3]])
        
        if st.button("🚀 GERAR ESTRATÉGIA"):
            # ROTA DE SEGURANÇA: Testamos a v1beta que é a única 100% aberta para Free Tier
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{"parts": [{"text": f"Resuma para marketing: {texto[:3000]}"}]}]
            }
            
            with st.spinner('Conectando ao Gemini Free...'):
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    res = response.json()
                    st.subheader("Sua Estratégia:")
                    st.write(res['candidates'][0]['content']['parts'][0]['text'])
                    st.balloons()
                elif response.status_code == 400:
                    st.error("Sua chave API está inválida. Gere uma nova no AI Studio.")
                else:
                    st.error(f"Erro {response.status_code}: O Google ainda não liberou sua chave.")
                    st.info("Dica: Vá ao AI Studio e clique em 'Create API Key in new project'.")
    except Exception as e:
        st.error(f"Erro técnico: {e}")
