import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="BoostEbook AI - Segredos Obscuros", page_icon="🧠")

# 2. ESTILO VISUAL (DARK MODE)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        background-color: #6a0dad; 
        color: white; 
        border-radius: 10px; 
        width: 100%; 
        font-weight: bold;
        height: 3em;
    }
    .stTextInput>div>div>input { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 BoostEbook AI")
st.subheader("Transforme seu Ebook em Marketing Viral")

# 3. GERENCIAMENTO DA API KEY (Prioriza Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Caso não esteja no Secrets, aparece o campo na lateral
    api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

# 4. FUNÇÃO PARA EXTRAIR TEXTO DE DIFERENTES FORMATOS
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
        st.error(f"Erro ao processar o arquivo: {e}")
    return None

# 5. LÓGICA PRINCIPAL DO APLICATIVO
if api_key:
    try:
        # Configura a IA
        genai.configure(api_key=api_key)
        
        # Modelo 'gemini-1.5-flash' é o mais estável para evitar o erro 404
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Upload de arquivos (Aceita PDF, Word e TXT)
        uploaded_file = st.file_uploader("Arraste seu arquivo aqui (PDF, DOCX ou TXT)", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            # Extração de conteúdo
            with st.spinner('Analisando documento...'):
                contexto = extrair_texto(uploaded_file)
            
            if contexto:
                st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")
                
                if st.button("Gerar Estratégia de Marketing"):
                    # Limitamos o texto enviado para a IA para evitar erros de limite de dados
                    texto_para_ia = contexto[:10000] 
                    
                    prompt = f"""
                    Você é um mestre do marketing digital e psicologia de vendas. 
                    Com base no conteúdo deste ebook: '{texto_para_ia}', crie:
                    1. Uma legenda hipnótica para Instagram.
                    2. Um roteiro de 15 segundos para Reels focado em viralizar.
                    3. 3 títulos impossíveis de ignorar para anúncios.
                    
                    Use um tom misterioso, elegante e altamente persuasivo.
                    """
                    
                    with st.spinner('A IA está criando sua campanha...'):
                        try:
                            response = model.generate_content(prompt)
                            st.markdown("---")
                            st.markdown("### 🚀 Sua Campanha Gerada:")
                            st.write(response.text)
                        except Exception as e_api:
                            st.error(f"Erro na geração da IA: {e_api}")
            else:
                st.warning("Não conseguimos ler o texto deste arquivo. Verifique se ele não está protegido por senha.")

    except Exception as e_config:
        st.error(f"Erro de configuração: {e_config}")
else:
    st.info("Aguardando configuração da API Key no painel lateral ou nos Secrets.")

# Rodapé informativo
st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para criadores de E-books estratégicos.")
