import streamlit as st
import requests
from PyPDF2 import PdfReader

# Configuração da Página
st.set_page_config(page_title="BoostEbook AI", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 BoostEbook AI")
st.subheader("Transforme seu PDF em Marketing Viral")

# 1. PEGA A CHAVE (A que você salvou corretamente agora!)
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Chave não encontrada nos Secrets. Verifique a digitação no painel do Streamlit.")
else:
    file = st.file_uploader("Arraste seu ebook aqui (PDF)", type=['pdf'])
    
    if file:
        with st.status("Lendo documento...", expanded=False) as status:
            try:
                reader = PdfReader(file)
                texto_completo = ""
                for page in reader.pages:
                    content = page.extract_text()
                    if content:
                        texto_completo += content
                status.update(label="Leitura concluída!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"Erro ao ler PDF: {e}")

        if st.button("🚀 GERAR ESTRATÉGIA DE MARKETING"):
            if not texto_completo:
                st.warning("O PDF parece estar vazio ou protegido.")
            else:
                with st.spinner('O Gemini está analisando seu conteúdo...'):
                    # URL V1BETA - A única que aceita gemini-1.5-flash sem erros de 'not found' hoje
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    
                    prompt = f"Analise o texto deste ebook e crie: 1. Um título irresistível, 2. Um post para Instagram com hashtags, 3. Um roteiro de 30 segundos para TikTok. Texto: {texto_completo[:4000]}"
                    
                    payload = {
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 800}
                    }
                    
                    try:
                        res = requests.post(url, json=payload)
                        if res.status_code == 200:
                            resultado = res.json()
                            texto_gerado = resultado['candidates'][0]['content']['parts'][0]['text']
                            
                            st.balloons()
                            st.markdown("---")
                            st.markdown("### 📈 Sua Estratégia Pronta:")
                            st.write(texto_gerado)
                            
                            st.download_button(
                                label="📥 Baixar Estratégia em TXT",
                                data=texto_gerado,
                                fileName="estrategia_marketing.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error(f"O Google respondeu com Erro {res.status_code}. Isso geralmente é um problema temporário na chave. Tente gerar o marketing novamente em 10 segundos.")
                    except Exception as e:
                        st.error(f"Falha na conexão: {e}")

st.markdown("---")
st.caption("Desenvolvido para criadores de Ebooks")
