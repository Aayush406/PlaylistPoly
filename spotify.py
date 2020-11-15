import spotipy
import os
from dotenv import load_dotenv
from spotipy import SpotifyOAuth
load_dotenv()
from collections import namedtuple

Playlist = namedtuple("Playlist", ["title", "tracks"])

scope = "playlist-read-private streaming user-read-email user-read-private user-read-playback-state user-modify-playback-state"

redirect_uri = os.getenv("REDIRECT_URI")


oauth = SpotifyOAuth(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"),
                                                    redirect_uri=redirect_uri, scope=scope, show_dialog=True,
                                                    open_browser=False)

sp_auth_link = oauth.get_authorize_url()

sp_main = spotipy.Spotify(auth_manager=oauth)

def format_playlists(json_data: [dict]) -> [dict]:
    formatted_playlists = []
    for playlist_data in json_data:
        key = playlist_data["name"]
        value = playlist_data["owner"]["display_name"]
        formatted_playlists.append(f"{key} by {value}")
    return formatted_playlists


def get_playlist_from_header(header: str, spot_playlist: [dict]) -> dict:
    for playlist in spot_playlist:
        if (header.startswith(playlist["name"])):
            return playlist
    return None


def formatted_track(track: dict):
    return f'"{track["name"]}" by {", ".join(artist["name"] for artist in track["artists"])}'


def final_playlist_format(playlist_data: dict, spotify_obj):
    title = playlist_data["name"]
    playlist_id = playlist_data["id"]
    playlist = spotify_obj.playlist_tracks(playlist_id)
    tracks = [formatted_track(track["track"]) for track in playlist["items"]]
    return Playlist(title=title, tracks=tracks)


def get_PlaylistPoly_device_id(spotify_obj):
    device_ids = spotify_obj.devices()["devices"]
    playlist_poly_id = [device["name"] for device in device_ids if device["name"] == "PlaylistPoly Player"]
    return playlist_poly_id[0]

def add_songs_to_queue(spotify_obj, playlist):
    playlist_id = playlist["id"]
    p = spotify_obj.playlist_tracks(playlist_id)
    print(p)
    for track in p["items"]:
        track_uri = f"spotify:track:{track['track']['href'][34:]}"
        spotify_obj.add_to_queue(track_uri)
    return

