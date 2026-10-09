import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')
API_KEY = os.getenv("API_KEY")
PART = 'contentDetails'
CHENNEL_HANDLE = 'MrBeast'
MAX_RESULT = 50
PLAY_LIST_ID = "UUX6OQ3DkcsbYNE6H8uQQuVA"

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



def get_video_ids(playlistId):
    video_ids = []
    pageToken = None
    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULT}&playlistId={playlistId}&key={API_KEY}'
     
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                    break

        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlistId = get_playlist_id()
    print(get_video_ids(playlistId))