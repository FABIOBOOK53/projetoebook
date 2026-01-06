import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="BoostEbook AI - Segredos Obscuros", page_icon="🧠")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #6a0dad; color: white; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 BoostEbook AI")
st.subheader("Transforme seu Ebook em Marketing Viral")

# Configuração da API Key
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

def extrair_texto(arquivo):
    nome_extensao = arquivo.name.lower()
    try:
        if nome_extensao.endswith('.txt'):
            return arquivo.read().decode("utf-8")
        elif nome_extensao.endswith('.pdf'):
            pdf_reader = PdfReader(arquivo)
            texto = ""
            for page in pdf_reader.pages:
                texto += page.extract_text() or ""
            return texto
        elif nome_extensao.endswith('.docx'):
            doc = Document(arquivo)
            return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
    return None

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # TENTATIVA AUTOMÁTICA DE MODELOS
        model_name = 'gemini-1.5-flash-latest' # Primeira opção (mais estável)
        model = genai.GenerativeModel(model_name)

        uploaded_file = st.file_uploader("Faça upload do seu Ebook (PDF, Word ou TXT)", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            contexto = extrair_texto(uploaded_file)
            
            if contexto:
                st.success("Conteúdo carregado!")
                if st.button("Gerar Estratégia de Marketing"):
                    prompt = f"Aja como um mestre do marketing. Baseado neste texto: '{contexto[:6000]}', crie 3 posts virais para Instagram e 1 roteiro de Reels. Tom misterioso."
                    
                    with st.spinner('Conectando com a mente da IA...'):
                        try:
                            response = model.generate_content(prompt)
                            st.markdown("---")
                            st.markdown("### 🚀 Sua Campanha Gerada:")
                            st.write(response.text)
                        except Exception as e:
                            # Se o primeiro modelo falhar, tenta o gemini-pro como backup
                            st.warning("Tentando modelo secundário...")
                            model_backup = genai.GenerativeModel('gemini-pro')
                            response = model_backup.generate_content(prompt)
                            st.write(response.text)
            else:
                st.warning("Arquivo vazio.")
    except Exception as e:
        st.error(f"Erro Crítico: {e}")
        st.info("Dica: Se o erro persistir, gere uma nova chave no Google AI Studio.")
else:
    st.info("Aguardando configuração da API Key.")
