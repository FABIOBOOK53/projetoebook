import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Força o uso da versão estável da API de 2026
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook", type=['pdf', 'docx'])
    
    if file:
        if st.button("🚀 GERAR ESTRATÉGIA"):
            with st.spinner('Conectando com Google Gemini...'):
                try:
                    # Chame o modelo direto pela string estável
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content("Diga: Conexão bem-sucedida!")
                    st.success(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro: {e}")
else:
    st.error("Configure a GOOGLE_API_KEY nos Secrets.")
