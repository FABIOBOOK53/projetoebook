import streamlit as st
import requests
from PyPDF2 import PdfReader

# Configuração da página
st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Puxa a chave dos Secrets do Streamlit
# Certifique-se de que no painel Secrets esteja: GOOGLE_API_KEY = "sua_chave"
api_key = st.secrets.get("GOOGLE_API_KEY")

file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file:
    if not api_key:
        st.error("⚠️ Erro: Chave API não encontrada nos Secrets do Streamlit.")
    else:
        try:
            # Leitura do PDF
            reader = PdfReader(file)
            # Extraímos apenas as primeiras páginas para garantir que a chave Free não trave
            texto_extraido = ""
            for i in range(min(5, len(reader.pages))):
                texto_extraido += reader.pages[i].extract_text() or ""
            
            if texto_extraido:
                st.success("✅ Documento lido com sucesso!")
                
                if st.button("🚀 GERAR ESTRATÉGIA"):
                    with st.spinner('A IA está analisando seu conteúdo...'):
                        # A URL exata que ignora as bibliotecas problemáticas
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                        
                        payload = {
                            "contents": [{
                                "parts": [{"text": f"Você é um especialista em marketing. Com base neste texto, crie uma estratégia de vendas: {texto_extraido[:3500]}"}]
                            }]
                        }
                        
                        # Chamada direta ao servidor do Google
                        response = requests.post(url, json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            # Extração do texto da resposta do Gemini
                            try:
                                resposta_final = data['candidates'][0]['content']['parts'][0]['text']
                                st.subheader("Sua Estratégia:")
                                st.write(resposta_final)
                                st.balloons()
                            except (KeyError, Index_Error):
                                st.error("O Google enviou uma resposta vazia. Verifique sua cota no AI Studio.")
                        elif response.status_code == 400:
                            st.error("❌ Erro 400: Chave API Inválida.")
                            st.info("Sua chave atual não foi reconhecida pelo Google. Por favor, gere uma nova no AI Studio e atualize seus Secrets.")
                        else:
                            st.error(f"Erro no servidor (Código {response.status_code})")
                            st.write(response.text)
            else:
                st.warning("Não foi possível extrair texto deste PDF. Verifique se ele não é apenas uma imagem.")
                
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")

# Rodapé informativo
st.markdown("---")
st.caption("BoostEbook AI - Versão Estável 2026")
