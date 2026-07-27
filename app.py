import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="Baixador de MP3 do YouTube",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Baixador de MP3 do YouTube")
st.write("Cole o link de qualquer vídeo do YouTube para extrair o áudio em MP3 instantaneamente.")

# Campo de entrada da URL
url_input = st.text_input("URL do Vídeo:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Converter para MP3", type="primary"):
    url_limpa = url_input.strip()
    
    if not url_limpa:
        st.warning("⚠️ Por favor, insira uma URL válida do YouTube.")
    else:
        with st.spinner("⚡ Conectando ao serviço e preparando o áudio..."):
            try:
                # Payload para a API do Cobalt pedir a conversão direta para MP3
                payload = {
                    "url": url_limpa,
                    "downloadMode": "audio",
                    "audioFormat": "mp3",
                    "audioBitrate": "320"
                }
                
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
                
                # Requisição à API pública do Cobalt
                response = requests.post(
                    "https://api.cobalt.tools/api/json",
                    json=payload,
                    headers=headers,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    
                    # Trata o retorno do link gerado
                    if status in ["tunnel", "redirect"]:
                        download_url = data.get("url")
                        
                        st.success("✅ Áudio convertido com sucesso!")
                        st.markdown(
                            f'<a href="{download_url}" target="_blank" style="text-decoration:none;">'
                            f'<button style="width:100%; height:50px; background-color:#4CAF50; color:white; '
                            f'border:none; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer;">'
                            f'⬇️ Clique aqui para baixar o MP3'
                            f'</button></a>',
                            unsafe_allow_html=True
                        )
                    else:
                        erro_msg = data.get("text", "Não foi possível processar este vídeo.")
                        st.error(f"❌ Erro do serviço: {erro_msg}")
                else:
                    st.error("❌ O serviço de conversão respondeu com erro. Verifique a URL e tente novamente.")

            except requests.exceptions.Timeout:
                st.error("⏱️ A requisição demorou muito para responder. Tente novamente em alguns segundos.")
            except Exception as e:
                st.error(f"❌ Ocorreu um erro ao processar o pedido: {e}")

# Rodapé simples
st.markdown("---")
st.caption("Ferramenta para conversão direta de áudio sem armazenar arquivos no servidor.")
