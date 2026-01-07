import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt

# Configuração da página
st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

# Chave vinda dos Segredos (Secrets)
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook", type=['pdf', 'docx'])
    
    if file:
        texto = ""
        try:
            # Extração de texto
            if file.type == "application/pdf":
                reader = PdfReader(file)
                texto = "".join([p.extract_text() or "" for p in reader.pages])
            else:
                texto = docx2txt.process(file)
            
            if texto:
                st.success("✅ Conteúdo lido!")
                
                if st.button("🚀 GERAR ESTRATÉGIA"):
                    with st.spinner('IA Processando...'):
                        try:
                            # Forma padrão e mais segura para Gemini 1.5 Flash
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            
                            # Prompt direto
                            response = model.generate_content(
                                f"Com base neste conteúdo, crie uma estratégia de marketing: {texto[:4000]}"
                            )
                            
                            st.subheader("Sua Estratégia:")
                            st.write(response.text)
                            st.balloons()
                        except Exception as e_api:
                            st.error(f"Erro na API: {e_api}")
        except Exception as e:
            st.error(f"Erro no processamento do arquivo: {e}")
else:
    st.error("Chave API não encontrada. Verifique os Secrets no Streamlit.")
