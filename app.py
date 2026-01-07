import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

# Chave API vinda dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # CONFIGURAÇÃO DE EMERGÊNCIA
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook", type=['pdf', 'docx'])
    
    if file:
        if st.button("🚀 GERAR ESTRATÉGIA"):
            with st.spinner('IA Processando...'):
                try:
                    # Forçando o uso do modelo estável sem o prefixo models/
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Teste direto com prompt simples
                    response = model.generate_content("Diga: Olá, o sistema está funcionando!")
                    
                    st.success("Conexão estabelecida!")
                    st.write(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro persistente: {e}")
else:
    st.error("Configure a GOOGLE_API_KEY nos Secrets.")
