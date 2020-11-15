import spotipy
import os
from dotenv import load_dotenv
from spotipy import SpotifyOAuth
load_dotenv()

scope = "playlist-read-private"
redirect_uri = "http://127.0.0.1:5000/spotify/callback"

sp_main = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"),
                                                    redirect_uri=redirect_uri, scope=scope))

user_playlists = sp_main.current_user_playlists()

for i, playlist in enumerate(user_playlists["items"]):
    print(i, playlist['name'])

while True:
    try:
        user_input = int(input("\nEnter the number of the playlist to view its songs: "))
        if user_input not in range(len(user_playlists["items"])):
            raise TypeError
        break
    except TypeError:
        print(f"Must be a number in the range 0-{len(user_playlists['items'])}")

selected_playlist = user_playlists["items"][user_input]["id"]
user_playlist = sp_main.playlist_tracks(selected_playlist)
print()
for i, track in enumerate(user_playlist["items"]):
    track = track["track"]
    print(i, f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")