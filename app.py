import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI - Vitoria", layout="centered")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")
file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    try:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() or "" for p in reader.pages[:3]])
        
        if st.button("🚀 GERAR ESTRATÉGIA"):
            # USANDO O MODELO QUE FUNCIONOU NO SEU CHAT (Gemini 3 Flash)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            
            payload = {"contents": [{"parts": [{"text": f"Crie uma estratégia de marketing para este livro: {texto[:3000]}"}]}]}
            
            with st.spinner('Acessando o modelo que você validou...'):
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    st.subheader("Sua Estratégia:")
                    st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                    st.balloons()
                else:
                    st.error(f"Erro {response.status_code}. Tente trocar 'gemini-3-flash-preview' por 'gemini-1.5-flash' no código.")
                    st.write("Detalhe técnico:", response.text)
    except Exception as e:
        st.error(f"Erro: {e}")
