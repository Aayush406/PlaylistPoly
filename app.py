from flask import Flask, render_template, request
from spotify import oauth, format_playlists, get_playlist_from_header, final_playlist_format
from spotipy import Spotify

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
        access_token = oauth.get_access_token(code=auth_code, as_dict=False)
        spot = Spotify(auth=access_token)
        user_playlists = format_playlists(spot.current_user_playlists()["items"])
        return render_template("playlists.html", playlists=user_playlists)

    return "YAY IT WORKED"

@app.route("/selections", methods=["POST"])
def spot_selections():
    global spot, playlist_1, playlist_2

    user_playlists = spot.current_user_playlists()["items"]
    selected_playlists = request.form.getlist("playlists")
    playlist_1, playlist_2 = [get_playlist_from_header(playlist, user_playlists) for playlist in selected_playlists]
    print(playlist_1)
    play1_format, play2_format = final_playlist_format(playlist_1, spot), final_playlist_format(playlist_2, spot)

    return render_template("prefinal_prompt.html", playlists=[play1_format, play2_format])

@app.route("/end", methods=["POST"])
def final_page():
    pass


if __name__ == '__main__':
    app.run(debug = True)
