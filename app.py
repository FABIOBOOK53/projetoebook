import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt

st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

# Puxando a chave nova que você criou
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook", type=['pdf', 'docx'])
    
    if file:
        texto = ""
        try:
            if file.type == "application/pdf":
                reader = PdfReader(file)
                texto = "".join([p.extract_text() or "" for p in reader.pages])
            else:
                texto = docx2txt.process(file)
            
            if texto:
                st.success("✅ Conteúdo lido!")
                if st.button("🚀 GERAR ESTRATÉGIA"):
                    with st.spinner('IA Processando...'):
                        # FORMA MAIS COMPATÍVEL DE TODAS:
                        try:
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            # Usando um prompt bem simples para teste
                            response = model.generate_content(f"Resuma em 3 tópicos: {texto[:2000]}")
                            st.write(response.text)
                            st.balloons()
                        except Exception as e_api:
                            st.error(f"Erro técnico na API: {e_api}")
        except Exception as e:
            st.error(f"Erro no arquivo: {e}")
else:
    st.error("Chave API não configurada nos Secrets.")
