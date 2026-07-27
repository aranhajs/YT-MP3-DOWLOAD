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
        status.text("⚡ Conectando ao YouTube e contornando travas de IP...")
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # pytubefix com client WEB_CREATOR/ANDROID para ignorar restrição de datacenter
                yt = YouTube(url, client='WEB_CREATOR')
                
                status.text(f"🎬 Vídeo encontrado: {yt.title}\nExtraindo o áudio...")
                
                # Filtra apenas a melhor faixa de áudio
                audio_stream = yt.streams.filter(only_audio=True).first()
                
                # Baixa o arquivo para a pasta temporária
                out_file = audio_stream.download(output_path=temp_dir)
                
                # Converte a extensão baixada (.m4a / .webm) para .mp3
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                
                # Lê os bytes para o botão de download do Streamlit
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

        except Exception as e:
            status.empty()
            st.error(f"❌ Não foi possível baixar este vídeo no momento. Detalhes do erro: {e}")

st.markdown("---")
st.caption("Conversor de Áudio Online com PyTubeFix.")
