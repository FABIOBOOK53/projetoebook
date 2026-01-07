import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt
import os

# Configuração da página
st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Busca a chave de API nos Secrets do Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # FORÇANDO A VERSÃO ESTÁVEL DA API PARA EVITAR ERRO 404
    os.environ["GOOGLE_API_VERSION"] = "v1" 
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
                        # Usando o nome do modelo sem o prefixo 'models/' 
                        # já que forçamos a versão v1 acima
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        try:
                            response = model.generate_content(f"Crie um post de marketing para: {texto[:4000]}")
                            st.subheader("Sua Estratégia:")
                            st.write(response.text)
                            st.balloons()
                        except Exception as ai_err:
                            st.error(f"Erro na chamada da IA: {ai_err}")
                            st.info("Dica: Verifique se sua chave API tem permissão para o modelo Gemini 1.5 Flash.")
                        
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
else:
    st.error("Erro: A GOOGLE_API_KEY não foi encontrada nos Secrets. Vá em Settings > Secrets no Streamlit Cloud.")
