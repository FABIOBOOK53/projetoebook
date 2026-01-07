import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt

st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # Configuração que força o uso da versão estável
        genai.configure(api_key=api_key)
        
        file = st.file_uploader("Suba seu ebook", type=['pdf', 'docx'])
        
        if file:
            texto = ""
            if file.type == "application/pdf":
                reader = PdfReader(file)
                texto = "".join([p.extract_text() or "" for p in reader.pages])
            else:
                texto = docx2txt.process(file)
            
            if texto:
                st.success("✅ Conteúdo lido!")
                if st.button("🚀 GERAR ESTRATÉGIA"):
                    with st.spinner('IA Processando...'):
                        # Mudança radical: usando o método direto da versão estável
                        # Se o erro 404 persistir aqui, o problema é 100% o requirements.txt
                        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                        
                        response = model.generate_content(
                            f"Crie um post de marketing para: {texto[:4000]}",
                            generation_config={"top_p": 0.95, "temperature": 0.7}
                        )
                        st.write(response.text)
                        st.balloons()
    except Exception as e:
        # Exibe o erro de forma mais limpa para identificarmos se é 404 ou outra coisa
        st.error(f"Houve um problema: {e}")
else:
    st.error("Configure a GOOGLE_API_KEY nos Secrets.")
