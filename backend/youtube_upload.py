```python
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
from googleapiclient.http import MediaFileUpload
from authentication import auth_token

youtube_video_id = None
playlist_id = None

def upload_youtube(mp4_video):
    global youtube_video_id, playlist_id

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=auth_token)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "10",
                "description": "Spectrogram visualization of audio file",
                "title": f"Spectrogram - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=MediaFileUpload(mp4_video)
    )

    response = request.execute()
    youtube_video_id = response['id']

    add_to_playlist(youtube)

def add_to_playlist(youtube):
    global playlist_id

    playlists_request = youtube.playlists().list(
        part="snippet",
        maxResults=25,
        mine=True
    )

    playlists_response = playlists_request.execute()

    for item in playlists_response["items"]:
        if item["snippet"]["title"] == datetime.now().strftime('%Y-%m-%d'):
            playlist_id = item["id"]
            break

    if playlist_id is None:
        playlist_request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": datetime.now().strftime('%Y-%m-%d'),
                    "description": "Playlist for today's audio files"
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        )

        playlist_response = playlist_request.execute()
        playlist_id = playlist_response['id']

    playlistitems_insert_request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": youtube_video_id
                }
            }
        }
    )

    playlistitems_insert_request.execute()
```