import streamlit as st
import requests
import json

st.set_page_config(page_title="Baixador MP3 Pro", page_icon="🎵")
st.title("🎵 Baixador de MP3")
st.write("Cole a URL do vídeo do YouTube para converter e extrair o áudio em alta qualidade.")

url_input = st.text_input("Link do vídeo (ex: https://www.youtube.com/watch?v=...):")

# Lista de instâncias da API pública do Cobalt para rotação em caso de bloqueio
APIS_DISPONIVEIS = [
    "https://api.cobalt.tools/api/json",
    "https://cobalt.qal.jp/api/json",
    "https://co.wuk.sh/api/json",
]

if st.button("Converter para MP3", type="primary"):
    url = url_input.strip()
    if not url:
        st.warning("⚠️ Por favor, insira uma URL válida.")
    else:
        status = st.empty()
        status.text("⚡ Conectando ao serviço de extração...")
        
        payload = {
            "url": url,
            "downloadMode": "audio",
            "audioFormat": "mp3",
            "audioBitrate": "320"
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        sucesso = False

        # Tenta em cada nó da API até encontrar uma rota ativa
        for api_url in APIS_DISPONIVEIS:
            if sucesso:
                break
            try:
                res = requests.post(api_url, json=payload, headers=headers, timeout=12)
                if res.status_code == 200:
                    data = res.json()
                    status_type = data.get("status")
                    
                    if status_type in ["tunnel", "redirect"]:
                        download_url = data.get("url")
                        
                        # Baixa o stream do áudio para permitir o botão st.download_button nativo do Streamlit
                        audio_res = requests.get(download_url, stream=True, timeout=30)
                        if audio_res.status_code == 200:
                            st.download_button(
                                label="⬇️ Baixar Arquivo MP3",
                                data=audio_res.content,
                                file_name="musica.mp3",
                                mime="audio/mpeg"
                            )
                            st.success("✅ Áudio pronto para download!")
                            status.empty()
                            sucesso = True
            except Exception:
                continue

        if not sucesso:
            st.error("❌ Não foi possível converter o vídeo no momento. O YouTube pode estar impondo restrições temporárias. Tente novamente em alguns instantes.")
            status.empty()

st.markdown("---")
st.caption("Conversor de Áudio Online com Rotação de NÓS.")
