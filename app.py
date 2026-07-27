import streamlit as st
import yt_dlp
import os
import tempfile
import time

# Título da Aplicação
st.set_page_config(page_title="Baixador MP3 Pro", page_icon="🎵")
st.title("🎵YouTube- MP3 DOWNLOAD - GRÁTIS -")
st.write("Cole a URL do vídeo abaixo para converter e baixar o áudio em tempo real.")

# Campo para o usuário colar o link
url_input = st.text_input("Link do vídeo (ex: https://www.youtube.com/watch?v=...)")

# Define onde salvar as mensagens de progresso
if 'progresso_msg' not in st.session_state:
    st.session_state.progresso_msg = "Aguardando início..."


# --- Configuração do Hook de Progresso ---
# Esta função é chamada pelo yt-dlp a cada atualização
def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            # Tenta extrair a porcentagem atual e converter para float
            p = d.get('_percent_str', '0%').replace('%', '')
            percentagem = float(p) / 100.0
            # Atualiza a barra de progresso no Streamlit
            barra_progresso.progress(percentagem)

            # Formata a mensagem de status (velocidade, tempo restante, etc)
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            status_text.text(f"Baixando: {p}% | Velocidade: {speed} | Restante: {eta}")
        except ValueError:
            pass
    elif d['status'] == 'finished':
        barra_progresso.progress(1.0)
        status_text.text("Download concluído! Iniciando conversão para MP3...")


# --- Botão de Ação ---
if st.button("Converter para MP3 em Tempo Real"):
    url = url_input.strip()
    if not url:
        st.warning("⚠️ Por favor, insira uma URL válida.")
    else:
        # Cria espaços na interface para serem atualizados dinamicamente
        status_text = st.empty()
        barra_progresso = st.progress(0.0)
        status_text.text("Conectando ao YouTube...")

        try:
            # Cria uma pasta temporária segura
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
    
    # === BURLAR BLOQUEIO DE DATACENTER/NUVEM ===
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'ios', 'mweb'],
            'skip': ['webpage', 'configs'],
        }
    },
    'http_headers': {
        'User-Agent': 'com.google.android.youtube/19.09.37 (Linux; U; Android 11; en_US) gzip',
    }
}

                # Executa o processo de download e conversão
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extrai informações (sem baixar) para pegar o nome do arquivo
                    info = ydl.extract_info(url, download=False)

                    # Inicia o download real (isso ativará o progress_hook)
                    ydl.download([url])

                    # Descobre o nome final do arquivo MP3 gerado
                    # (Mesmo nome base do vídeo, mas extensão .mp3)
                    filename = ydl.prepare_filename(info)
                    mp3_filename = os.path.splitext(filename)[0] + ".mp3"

                # Verifica se o arquivo final realmente existe
                if os.path.exists(mp3_filename):
                    # Fornece o arquivo para download no navegador
                    with open(mp3_filename, "rb") as file:
                        # Lê os dados do arquivo
                        file_bytes = file.read()

                        # Mostra o botão de download
                        st.download_button(
                            label="⬇️ Baixar Arquivo MP3 Gerado",
                            data=file_bytes,
                            file_name=os.path.basename(mp3_filename),
                            mime="audio/mpeg"
                        )
                    st.success("✅ Tudo pronto! Clique no botão acima para baixar.")
                    status_text.empty()  # Limpa o texto de status
                else:
                    st.error("Erro interno: O arquivo MP3 não foi gerado.")

        except Exception as e:
            st.error(f"❌ Ocorreu um erro ao processar o vídeo: {e}")
            # Limpa a barra em caso de erro
            if 'barra_progresso' in locals():
                barra_progresso.empty()
            if 'status_text' in locals():
                status_text.empty()

# Rodapé simples
st.markdown("---")
st.caption("Desenvolvido com ❤️ #Aranha-Developer")
