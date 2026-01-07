import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt

# Configuração da página
st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

# Busca a chave de API nos Secrets do Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # Upload de arquivos
    file = st.file_uploader("Suba seu ebook", type=['pdf', 'docx'])
    
    if file:
        texto = ""
        try:
            # Processamento de PDF
            if file.type == "application/pdf":
                reader = PdfReader(file)
                texto = "".join([p.extract_text() or "" for p in reader.pages])
            # Processamento de Word
            else:
                texto = docx2txt.process(file)
            
            if texto:
                st.success("✅ Conteúdo lido!")
                
                if st.button("🚀 GERAR ESTRATÉGIA"):
                    with st.spinner('IA Processando...'):
                        # --- LINHA CORRIGIDA ABAIXO ---
                        # Adicionado 'models/' antes do nome para evitar erro 404
                        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
                        
                        # Chamada da API com o texto extraído (limitado a 4000 caracteres para segurança)
                        response = model.generate_content(f"Crie um post de marketing para: {texto[:4000]}")
                        
                        st.subheader("Sua Estratégia:")
                        st.write(response.text)
                        st.balloons()
                        
        except Exception as e:
            st.error(f"Erro ao processar arquivo ou gerar conteúdo: {e}")
else:
    st.error("Erro: A GOOGLE_API_KEY não foi encontrada nos Secrets do Streamlit.")
