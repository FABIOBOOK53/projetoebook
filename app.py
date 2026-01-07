import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document
import io

st.set_page_config(page_title="BoostEbook AI - Pro", layout="centered")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

# Aceita PDF e DOCX agora
file = st.file_uploader("Suba seu ebook (PDF ou DOCX)", type=['pdf', 'docx'])

def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        return "".join([p.extract_text() or "" for p in reader.pages[:5]])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs[:50]]) # Aproximadamente 5 páginas
    return None

if file and api_key:
    try:
        texto = extract_text(file)
        
        if texto:
            st.success(f"✅ Arquivo {file.name} lido com sucesso!")
            
            # PROMPT TURBINADO: Agora pede roteiros de ASMR e Reels
            prompt_vendas = f"""
            Você é um estrategista de marketing viral. Com base neste livro: {texto[:3500]}
            1. Crie 3 roteiros curtos (15s) para Reels/TikTok focados em curiosidade.
            2. Crie 1 roteiro de vídeo sensorial (ASMR) para YouTube Shorts.
            3. Escreva um e-mail de venda 'irresistível' para quem gosta deste gênero literário.
            """
            
            if st.button("🚀 GERAR ESTRATÉGIA COMPLETA"):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
                
                with st.spinner('A IA está criando seus roteiros...'):
                    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt_vendas}]}]})
                    
                    if response.status_code == 200:
                        st.subheader("Sua Estratégia de Conteúdo:")
                        st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                        st.balloons()
                    else:
                        st.error(f"Erro na conexão. Status: {response.status_code}")
    except Exception as e:
        st.error(f"Erro técnico: {e}")
