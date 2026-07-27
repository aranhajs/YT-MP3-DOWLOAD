import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Baixador MP3 Pro", page_icon="🎵")
st.title("🎵 Baixador de MP3")
st.write("O áudio é processado diretamente pelo seu navegador, evitando restrições de IP.")

url_input = st.text_input("Link do vídeo do YouTube:")

if st.button("Gerar Download", type="primary"):
    url = url_input.strip()
    if not url:
        st.warning("⚠️ Insira uma URL válida.")
    else:
        st.info("⚡ Processando pelo seu navegador...")
        
        # Componente HTML/JS que executa no lado do cliente (IP do Usuário)
        js_code = f"""
        <script>
            async function downloadAudio() {{
                const videoUrl = "{url}";
                try {{
                    // Usa a API do Cobalt acionada do IP do cliente
                    const response = await fetch("https://api.cobalt.tools/api/json", {{
                        method: "POST",
                        headers: {{
                            "Accept": "application/json",
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify({{
                            url: videoUrl,
                            downloadMode: "audio",
                            audioFormat: "mp3"
                        }})
                    }});
                    
                    const data = await response.json();
                    
                    if (data.status === "tunnel" || data.status === "redirect") {{
                        // Dispara o download diretamente no navegador do usuário
                        window.open(data.url, '_blank');
                    }} else {{
                        alert("Erro ao converter o vídeo: " + (data.text || "Vídeo indisponível"));
                    }}
                }} catch (err) {{
                    alert("Erro de rede ao conectar com o conversor.");
                }}
            }}
            downloadAudio();
        </script>
        """
        components.html(js_code, height=0)
        st.success("✅ Solicitação enviada! Se o download não iniciar automaticamente, verifique se o seu navegador bloqueou pop-ups.")

st.markdown("---")
st.caption("Processamento via Client-Side (IP do Usuário).")
