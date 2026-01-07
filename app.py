import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt

st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Suporte a PDF e Word conforme sua necessidade
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
                        # Linha definitiva que ignora o erro 404 de URL
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(f"Crie um post de marketing para: {texto[:4000]}")
                        st.write(response.text)
                        st.balloons()
        except Exception as e:
            st.error(f"Erro: {e}")
else:
    st.error("Configure a GOOGLE_API_KEY nos Secrets.")
