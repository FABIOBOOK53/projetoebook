import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt

# Configuração da página
st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # 1. Configuração direta
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
                        try:
                            # 2. MUDANÇA CRUCIAL: Forçando o uso do modelo via string direta na SDK estável
                            # Esta forma evita que ele tente usar o endpoint 'v1beta'
                            model = genai.GenerativeModel('models/gemini-1.5-flash')
                            
                            # 3. Limpeza simples no texto para evitar caracteres especiais que travam a API
                            prompt_seguro = f"Crie um post de marketing para o seguinte conteúdo: {texto[:3000]}"
                            
                            response = model.generate_content(prompt_seguro)
                            
                            if response.text:
                                st.subheader("Sua Estratégia:")
                                st.write(response.text)
                                st.balloons()
                            else:
                                st.warning("A IA não retornou texto. Verifique os créditos da sua API.")
                                
                        except Exception as e_ia:
                            # Se der erro 404 aqui, o problema está na versão da biblioteca instalada
                            st.error(f"Erro na API Google: {e_ia}")
                            st.info("Sugestão: Adicione 'google-generativeai>=0.8.0' no seu arquivo requirements.txt")
                            
        except Exception as e:
            st.error(f"Erro no processamento: {e}")
else:
    st.error("Configure a GOOGLE_API_KEY nos Secrets do Streamlit.")
