from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")


client = WebClient(token=SLACK_BOT_TOKEN)

def get_channel_id_by_name(channel_name):
    try:
        response = client.conversations_list()
        for channel in response["channels"]:
            if channel["name"] == channel_name:
                return channel["id"]
        return None
    except SlackApiError as e:
        print("Error al obtener canales (revisar que sí se llame así):", e.response["error"])
        return None

def send_slack_message(channel, text):
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        return response["ok"]
    except SlackApiError as e:
        print("Error al mandar el mensaje:", e.response["error"])
        return False

def send_slack_file(channel_name, filepath, title="Archivo"):
    try:
        channel_id = get_channel_id_by_name(channel_name)
        print(f"Canal '{channel_name}' tiene ID: {channel_id}")

        if not channel_id:
            print("No se encontró el ID del canal")
            return False

        with open(filepath, "rb") as file_content:
            response = client.files_upload_v2(
                file_uploads=[{
                    "file": file_content,
                    "filename": title,
                    "title": title,
                    "channels": [channel_id]
                }],
                initial_comment="Archivo subido desde Streamlit"
            )

        uploaded = response["files"][0]
        file_link = uploaded.get("permalink")
        published_channels = uploaded.get("channels", [])

        if not published_channels:
            #Aquí se intenta publicar manualmente el archivo
            client.chat_postMessage(
                channel=channel_id,
                text=f"Archivo subido: <{file_link}>"
            )
            print("Archivo subido y publicado manualmente.")
        else:
            print("Archivo subido y publicado automáticamente.")

        return True

    except SlackApiError as e:
        print("Error al subir archivo:", e.response["error"])
        return False
    except Exception as ex:
        print("Error inesperado:", ex)
        return False

def send_image_url(channel, image_url, title="Imagen desde URL"):
    try:
        response = client.chat_postMessage(
            channel=channel,
            blocks=[
                {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": title
                }
            ],
            text=title
        )
        return response["ok"]
    except SlackApiError as e:
        print("Error al enviar imagen:", e.response["error"])
        return False
