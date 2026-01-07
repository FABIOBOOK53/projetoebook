import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI - Final")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Configuração direta
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])
    
    if file:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() for p in reader.pages])
        st.success("✅ Texto lido!")
        
        if st.button("🚀 GERAR ESTRATÉGIA"):
            with st.spinner('IA Processando...'):
                try:
                    # Trocamos para o modelo PRO, que possui rotas v1 mais estáveis
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = model.generate_content(f"Crie um post de marketing: {texto[:3000]}")
                    st.write(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro na IA: {e}")
else:
    st.error("Chave API não configurada.")
