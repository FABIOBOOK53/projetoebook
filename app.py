import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI - Final", layout="centered")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")
file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    try:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() or "" for p in reader.pages[:3]])
        
        if st.button("🚀 GERAR ESTRATÉGIA"):
            # Usando v1beta que é a rota mais estável para chaves novas
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {"contents": [{"parts": [{"text": f"Resuma para marketing: {texto[:3000]}"}]}]}
            
            with st.spinner('Validando nova chave...'):
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    st.subheader("Sua Estratégia:")
                    st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                    st.balloons()
                else:
                    st.error(f"Erro {response.status_code}: O Google ainda não reconheceu esta nova chave.")
                    st.write("Aguarde 2 minutos e tente novamente.")
    except Exception as e:
        st.error(f"Erro no PDF: {e}")
