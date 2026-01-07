import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt

# Configuração da página
st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Puxa a chave dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # --- A MUDANÇA QUE RESOLVE O 404 ---
    # Forçamos a configuração básica e usamos o nome do modelo SEM prefixos
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
                    with st.spinner('A IA está trabalhando...'):
                        try:
                            # Em 2026, usar apenas o nome simples resolve o conflito v1beta
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            
                            # Chamada direta
                            response = model.generate_content(
                                f"Com base neste texto, crie uma estratégia de marketing: {texto[:4000]}"
                            )
                            
                            st.subheader("Sua Estratégia:")
                            st.write(response.text)
                            st.balloons()
                        except Exception as e_ia:
                            st.error(f"Erro na IA: {e_ia}")
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
else:
    st.error("Chave API não configurada nos Secrets.")
