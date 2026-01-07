import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Puxa a chave que você colocou no 'Secrets' do Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    try:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() or "" for p in reader.pages])
        
        if texto:
            st.success("✅ Documento lido com sucesso!")
            
            if st.button("🚀 GERAR ESTRATÉGIA"):
                # URL oficial e estável de 2026 para o Gemini 1.5 Flash
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{"parts": [{"text": f"Crie um resumo de marketing para: {texto[:3500]}"}]}]
                }
                
                with st.spinner('IA Processando...'):
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        res = response.json()
                        st.subheader("Sua Estratégia:")
                        st.write(res['candidates'][0]['content']['parts'][0]['text'])
                        st.balloons()
                    elif response.status_code == 404:
                        st.error("Erro 404: O Google não reconheceu este modelo na sua região.")
                    else:
                        st.error(f"Erro {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Erro técnico: {e}")
else:
    if not api_key:
        st.warning("⚠️ Chave API não encontrada. Vá em Settings -> Secrets no Streamlit.")
