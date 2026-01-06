import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# 1. Configura a chave vinda dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])
    if file:
        try:
            reader = PdfReader(file)
            texto = "".join([p.extract_text() or "" for p in reader.pages])
            st.success("✅ PDF lido com sucesso!")
            
            if st.button("🚀 GERAR ESTRATÉGIA DE MARKETING"):
                with st.spinner('A IA está trabalhando...'):
                    # USANDO O MODELO MAIS ESTÁVEL DO MUNDO
                    model = genai.GenerativeModel('gemini-pro')
                    
                    prompt = f"Crie uma estratégia de marketing viral para este livro: {texto[:4000]}"
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.markdown("### 📈 Sua Estratégia:")
                    st.write(response.text)
                    st.balloons()
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
else:
    st.error("⚠️ Configure a GOOGLE_API_KEY nos Secrets.")
