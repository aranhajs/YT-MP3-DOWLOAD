import streamlit as st
import urllib.parse

st.set_page_config(page_title="Baixador MP3 Pro", page_icon="🎵")
st.title("🎵 Baixador de MP3")
st.write("Cole o link do vídeo do YouTube para gerar o botão de download direto via IP do seu navegador.")

url_input = st.text_input("Link do vídeo (ex: https://www.youtube.com/watch?v=...):")

if st.button("Gerar Link de Download", type="primary"):
    url = url_input.strip()
    if not url:
        st.warning("⚠️ Por favor, insira uma URL válida.")
    else:
        # Codifica a URL com segurança para não quebrar os parâmetros HTTP
        url_encoded = urllib.parse.quote(url, safe='')
        
        # Link de processamento do Cobalt acionado no lado do cliente
        cobalt_web_url = f"https://cobalt.tools/#url={url_encoded}"
        
        st.success("✅ Link de extração gerado com sucesso!")
        st.info("Para contornar os bloqueios de IP do servidor do YouTube, o processamento ocorre via requisição do seu próprio navegador.")
        
        # Botão estilizado de redirecionamento direto
        st.markdown(
            f'''
            <a href="{cobalt_web_url}" target="_blank" style="text-decoration: none;">
                <button style="
                    width: 100%;
                    background-color: #4CAF50;
                    color: white;
                    padding: 14px 20px;
                    margin: 8px 0;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: bold;
                ">
                    🚀 Clique aqui para abrir a página de download (MP3)
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Processamento direto no lado do cliente (Client-Side).")
