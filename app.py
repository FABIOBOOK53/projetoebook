import streamlit as st
import requests
from PyPDF2 import PdfReader

# Configuração visual básica
st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")
st.markdown("---")

# 1. Busca a chave que você salvou nos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Chave GOOGLE_API_KEY não encontrada nos Secrets do Streamlit.")
else:
    # 2. Upload do arquivo
    file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])
    
    if file:
        try:
            reader = PdfReader(file)
            # Extrai o texto de todas as páginas
            texto = "".join([p.extract_text() or "" for p in reader.pages])
            
            if texto:
                st.success("✅ PDF lido com sucesso!")
                
                # 3. Botão para acionar a IA
                if st.button("🚀 GERAR ESTRATÉGIA DE MARKETING"):
                    with st.spinner('A IA está analisando seu livro...'):
                        
                        # URL de alta compatibilidade para evitar erro 404
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
                        
                        payload = {
                            "contents": [{
                                "parts": [{"text": f"Aja como um especialista em marketing digital. Com base no texto a seguir, crie 3 posts para Instagram e 1 roteiro de Reels para vender este livro: {texto[:4000]}"}]
                            }]
                        }
                        
                        # Chamada para o Google
                        response = requests.post(url, json=payload)
                        
                        if response.status_code == 200:
                            dados = response.json()
                            st.markdown("---")
                            st.markdown("### 📈 Sua Estratégia Pronta:")
                            st.write(dados['candidates'][0]['content']['parts'][0]['text'])
                            st.balloons()
                        else:
                            # Mostra o erro real se algo falhar
                            st.error(f"Erro {response.status_code}: {response.text}")
            else:
                st.warning("Não foi possível extrair texto deste PDF. Ele pode ser uma imagem.")
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")

st.markdown("---")
st.caption("BoostEbook AI - Versão 2026")
