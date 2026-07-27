import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Baixador MP3 Pro", page_icon="🎵")
st.title("🎵 Baixador de MP3")
st.write("Cole a URL do vídeo abaixo para converter e baixar o áudio.")

url_input = st.text_input("Link do vídeo:")

def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            p = d.get('_percent_str', '0%').replace('%', '').strip()
            percentagem = float(p) / 100.0
            barra_progresso.progress(min(max(percentagem, 0.0), 1.0))
            speed = d.get('_speed_str', 'N/A')
            status_text.text(f"Baixando: {p}% | Velocidade: {speed}")
        except ValueError:
            pass
    elif d['status'] == 'finished':
        barra_progresso.progress(1.0)
        status_text.text("Download concluído! Finalizando arquivo MP3...")

if st.button("Converter para MP3", type="primary"):
    url = url_input.strip()
    if not url:
        st.warning("⚠️ Insira uma URL válida.")
    else:
        status_text = st.empty()
        barra_progresso = st.progress(0.0)
        status_text.text("Conectando e ignorando travas de IP...")

        # Lista de proxies/instâncias para contornar o bloqueio de datacenter
        lista_proxies = [None, 'https://inv.tux.pizza', 'https://invidious.nerdvpn.de']
        sucesso = False

        for proxy in lista_proxies:
            if sucesso:
                break
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                        'progress_hooks': [progress_hook],
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['ios', 'mweb'],
                                'player_skip': ['webpage', 'configs'],
                            }
                        },
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
                        }
                    }

                    if proxy:
                        ydl_opts['proxy'] = proxy

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        mp3_filename = os.path.splitext(filename)[0] + ".mp3"

                        if os.path.exists(mp3_filename):
                            with open(mp3_filename, "rb") as file:
                                file_bytes = file.read()
                                st.download_button(
                                    label="⬇️ Baixar Arquivo MP3",
                                    data=file_bytes,
                                    file_name=os.path.basename(mp3_filename),
                                    mime="audio/mpeg"
                                )
                            st.success("✅ Áudio gerado com sucesso!")
                            status_text.empty()
                            sucesso = True
            except Exception as e:
                # Tenta o próximo proxy se falhar
                continue

        if not sucesso:
            st.error("❌ O YouTube bloqueou a requisição em todas as rotas. Tente novamente em alguns instantes ou verifique se o link está correto.")
            barra_progresso.empty()
            status_text.empty()

st.markdown("---")
st.caption("Conversor de Áudio Online.")
