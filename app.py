import streamlit as st
from pytubefix import YouTube
import os
import tempfile

st.set_page_config(page_title="Baixador MP3 Pro", page_icon="🎵")
st.title("🎵 Baixador de MP3")
st.write("Cole o link do vídeo do YouTube para converter e baixar o áudio em MP3.")

url_input = st.text_input("Link do vídeo:")

if st.button("Converter para MP3", type="primary"):
    url = url_input.strip()
    if not url:
        st.warning("⚠️ Por favor, insira uma URL válida.")
    else:
        status = st.empty()
        status.text("⚡ Conectando ao YouTube e contornando autenticação...")
        
        # Lista de clientes que não exigem login para faixas de áudio
        clientes = ['TV_EMBEDDED', 'WEB_EMBEDDED', 'ANDROID_TESTSUITE']
        sucesso = False
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for cliente in clientes:
                if sucesso:
                    break
                try:
                    status.text(f"Tentando extrair áudio (Modo: {cliente})...")
                    yt = YouTube(url, client=cliente)
                    
                    audio_stream = yt.streams.filter(only_audio=True).first()
                    if not audio_stream:
                        audio_stream = yt.streams.get_audio_only()

                    if audio_stream:
                        out_file = audio_stream.download(output_path=temp_dir)
                        
                        base, ext = os.path.splitext(out_file)
                        new_file = base + '.mp3'
                        os.rename(out_file, new_file)
                        
                        with open(new_file, 'rb') as f:
                            audio_bytes = f.read()
                        
                        status.empty()
                        st.success(f"✅ **{yt.title}** convertido com sucesso!")
                        
                        st.download_button(
                            label="⬇️ Baixar Arquivo MP3",
                            data=audio_bytes,
                            file_name=f"{yt.title}.mp3",
                            mime="audio/mpeg"
                        )
                        sucesso = True
                except Exception as e:
                    continue

            if not sucesso:
                status.empty()
                st.error("❌ O YouTube exigiu autenticação de conta para este vídeo específico. Tente outro link ou tente novamente em instantes.")

st.markdown("---")
st.caption("Conversor de Áudio Online.")
