import streamlit as st
from slack_utils import send_slack_message, send_slack_file, send_image_url
import os

st.set_page_config(page_title="Slack Bot Equipo 45")
st.title("Slack Bot desde Streamlit")
st.write("Sprint 1 (Design & Architecture)")
st.write("La aplicación de Python se usará para hacer envío a Slack de: Mensajes, Imágenes por URL y Archivos.")

channel = st.text_input("Aquí poner el canal en el que el bot va a mandar el mensaje (no poner #)", value="general")

# --- Mandar mensaje ---
st.header("Enviar mensaje")
with st.form("Enviar mensaje"):
    text = st.text_area("Escribe lo que quieres enviar")
    send_msg = st.form_submit_button("Enviar mensaje")
    if send_msg:
        if send_slack_message(channel, text):
            st.success("El mensaje fue enviado")
        else:
            st.error("El mensaje falló al ser enviado")
            st.caption("Revisar consola")

# --- Url para foto ---
st.header("Enviar URL para imagen")
with st.form("Enviar imagen"):
    img_url = st.text_input("Pega la URL de la imagen (antes leer instrucciones.txt)")
    send_img = st.form_submit_button("Enviar imagen")
    if send_img and img_url:
        if any(img_url.lower().endswith(ext) for ext in [".jpg", ".png", ".jpeg", ".gif"]):
            if send_image_url(channel, img_url, title="Imagen enviada"):
                st.success("Imagen enviada correctamente")
            else:
                st.error("Falló el envío de la imagen")
                st.caption("Hay que ver que sí sea pública la url (revisar instrucciones.txt)")
        else:
            st.warning("Revisar instrucciones.txt para saber el formato de la url")

# --- Mandar archivo ---
st.header("Mandar archivo")
with st.form("Enviar archivo"):
    file = st.file_uploader("Sube un archivo")
    send_file = st.form_submit_button("Enviar archivo")
    if send_file and file:
        temp_path = os.path.join("temp_" + file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())

        success = send_slack_file(channel, temp_path, title=file.name)
        os.remove(temp_path)

        if success:
            st.success("Archivo subido correctamente y publicado en Slack")
        else:
            st.error("El archivo fue subido pero no se publicó automáticamente.")
            st.caption("Se intentó publicar manualmente con un enlace.")
