import os
from dotenv import load_dotenv
import spotipy
from base64 import b64encode
import requests


def load_image_b64(uri):
    res = requests.get(uri)
    return b64encode(res.content).decode('ascii')


def prevent_ampersand(text):
    return ''.join([elem if elem != '&' else 'and' for elem in text])


def get_current_song():

    load_dotenv()

    USER_NAME = os.getenv('USER_NAME')

    scope = ['user-read-recently-played']

    token = spotipy.util.prompt_for_user_token(
        USER_NAME, scope, redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'))

    if token:
        sp = spotipy.Spotify(auth=token)
        current_song_info = sp.current_user_recently_played(limit=1)
        current_song_uri = current_song_info['items'][0]['track']['uri']
    else:
        print('err')

    current_song = sp.track(current_song_uri)

    song_name = prevent_ampersand(current_song['name'])
    album_name = prevent_ampersand(current_song['album']['name'])
    artists = ', '.join([prevent_ampersand(artist['name'])
                         for artist in current_song['artists']])
    album_cover = load_image_b64(current_song['album']['images'][0]['url'])
    href = current_song['external_urls']['spotify']
    spotify_logo = load_image_b64(
        'https://cdn.icon-icons.com/icons2/836/PNG/512/Spotify_icon-icons.com_66783.png')

    return {'song_name': song_name,
            'album_name': album_name,
            'artists': artists,
            'album_cover': album_cover,
            'href': href,
            'spotify_logo': spotify_logo}
