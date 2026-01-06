import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Puxa a chave dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("Cole sua API Key aqui", type="password")

def extrair_texto(arquivo):
    ext = arquivo.name.lower()
    try:
        if ext.endswith('.pdf'):
            return "".join([p.extract_text() or "" for p in PdfReader(arquivo).pages])
        if ext.endswith('.docx'):
            return "\n".join([p.text for p in Document(arquivo).paragraphs])
        return arquivo.read().decode("utf-8")
    except: return None

if api_key:
    uploaded_file = st.file_uploader("Upload do seu Ebook", type=['txt', 'pdf', 'docx'])
    
    if uploaded_file:
        texto = extrair_texto(uploaded_file)
        if texto:
            st.success("Arquivo carregado com sucesso!")
            if st.button("Gerar Marketing Viral"):
                with st.spinner('A IA está lendo seu livro...'):
                    # USAMOS A URL ESTÁVEL (v1) QUE O CHAT DO STUDIO USA
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    payload = {
                        "contents": [{
                            "parts": [{"text": f"Aja como um mestre do marketing digital. Com base neste texto, crie 3 posts para Instagram e 2 títulos de anúncios: {texto[:5000]}"}]
                        }]
                    }
                    
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        st.markdown("### 🚀 Estratégia de Marketing:")
                        st.write(res_data['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Erro na conexão (Status {response.status_code}). Verifique se a chave nos Secrets está correta.")
else:
    st.info("Por favor, configure a chave API no menu lateral ou nos Secrets.")
