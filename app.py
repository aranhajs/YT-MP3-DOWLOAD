import streamlit as st
import requests

st.set_page_config(page_title="Baixador MP3 Pro", page_icon="🎵")
st.title("🎵 Baixador de MP3")
st.write("Cole a URL do vídeo do YouTube abaixo para gerar o download direto do MP3.")

url_input = st.text_input("Link do vídeo (ex: https://www.youtube.com/watch?v=...):")

if st.button("Gerar Download", type="primary"):
    url = url_input.strip()
    if not url:
        st.warning("⚠️ Insira uma URL válida.")
    else:
        status = st.empty()
        status.info("⚡ Extraindo áudio através do servidor proxy...")
        
        # Extrai o ID do vídeo da URL colada
        video_id = None
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            
        if not video_id:
            st.error("❌ Formato de URL inválido. Use um link padrão do YouTube.")
        else:
            # Lista de instâncias públicas do Invidious para tentar o bypass do IP
            instancias = [
                "https://inv.tux.pizza",
                "https://invidious.nerdvpn.de",
                "https://yt.drgnz.club"
            ]
            
            audio_url = None
            titulo = "audio_youtube"
            
            for inst in instancias:
                try:
                    # Consulta os dados e os links de mídia diretamente na API da instância
                    api_url = f"{inst}/api/v1/videos/{video_id}"
                    res = requests.get(api_url, timeout=8)
                    
                    if res.status_code == 200:
                        data = res.json()
                        titulo = data.get("title", "musica")
                        adaptive_formats = data.get("adaptiveFormats", [])
                        
                        # Filtra apenas as faixas de áudio
                        audio_streams = [f for f in adaptive_formats if "audio" in f.get("type", "")]
                        if audio_streams:
                            # Pega a melhor qualidade disponível
                            audio_url = audio_streams[0].get("url")
                            break
                except Exception:
                    continue

            status.empty()
            if audio_url:
                st.success(f"✅ **{titulo}** pronto para download!")
                
                # Exibe o botão direto de download do MP3 no seu app
                st.markdown(
                    f'''
                    <a href="{audio_url}" target="_blank" download="{titulo}.mp3" style="text-decoration: none;">
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
                            ⬇️ Baixar Arquivo de Áudio (MP3)
                        </button>
                    </a>
                    ''',
                    unsafe_allow_html=True
                )
            else:
                st.error("❌ Não foi possível extrair o áudio no momento. Tente novamente em alguns instantes.")

st.markdown("---")
st.caption("Conversor de Áudio via Instâncias Espelho.")
