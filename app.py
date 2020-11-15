from flask import Flask, render_template, request
from spotify import oauth, format_playlists, get_playlist_from_header, final_playlist_format, add_songs_to_queue, get_PlaylistPoly_device_id
from spotipy import Spotify

# 1416d4f6efe454c3a10311e784f0738ab0cee929

app = Flask(__name__)

spot = None
playlist_1 = None
playlist_2 = None
access_token = None

@app.route('/')
def home():
    return render_template("home.html", spotify_login=oauth.get_authorize_url())


@app.route("/spotify/callback")
def sp_page():
    auth_code = request.args.get("code")
    if auth_code != None:
        global spot, access_token
        access_token = oauth.get_access_token(code=auth_code, as_dict=False, check_cache=False)
        spot = Spotify(auth=access_token)
        user_playlists = format_playlists(spot.current_user_playlists()["items"])
        return render_template("playlists.html", playlists=user_playlists)
    return render_template("home.html", spotify_login=oauth.get_authorize_url())

@app.route("/selections", methods=["POST"])
def spot_selections():
    global spot, playlist_1, playlist_2

    user_playlists = spot.current_user_playlists()["items"]
    selected_playlists = request.form.getlist("playlists")

    playlist_1, playlist_2 = [get_playlist_from_header(playlist, user_playlists) for playlist in selected_playlists]
    play1_format, play2_format = final_playlist_format(playlist_1, spot), final_playlist_format(playlist_2, spot)

    return render_template("prefinal_prompt.html", p1=play1_format, p2=play2_format)


@app.route("/end", methods=["POST"])
def final_page():
    confirm = dict(request.form)
    global spot, playlist_1, playlist_2, access_token
    add_songs_to_queue(spot, playlist_1)
    add_songs_to_queue(spot, playlist_2)
    return render_template("final.html", token=access_token)


if __name__ == '__main__':
    app.run(debug = True)
