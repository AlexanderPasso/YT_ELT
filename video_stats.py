import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')
API_KEY = os.getenv("API_KEY")
PART = 'contentDetails'
CHENNEL_HANDLE = 'MrBeast'

#Codigo para obtener el ID de la lista de reproducción

def get_playlist_id():

    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part={PART}&forHandle={CHENNEL_HANDLE}&key={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        #print(json.dumps(data, indent=4))

        chennel_items = data["items"][0]
        channel_playlisId = chennel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlisId)
        return channel_playlisId
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    get_playlist_id()

        