import spotipy
import os
from dotenv import load_dotenv
from spotipy import SpotifyOAuth
load_dotenv()

scope = "user-library-read"
redirect_uri = "http://127.0.0.1:5000/spotify/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri=redirect_uri, scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])