import requests
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

# ====================================================== DATE =======================================================#
current_date = datetime.now()
past_date = current_date - timedelta(30)
amended_date = past_date.strftime("%Y-%m-%d")
amended_year = past_date.strftime("%Y")

# ==================================================== BILLBOARD =====================================================#
billboard_url = "https://www.billboard.com/charts/hot-100"
response = requests.get(f"{billboard_url}/{amended_date}")
response_text = response.text
soup = BeautifulSoup(response_text, "html.parser")
billboard_response = soup.find_all(name="span", class_="chart-element__information__song")

billboard_songs = []
for b_songs in billboard_response:
    all_songs = b_songs.getText()
    billboard_songs.append(all_songs)

# ====================================================  SPOTIFY  =====================================================#
spotify_client_id = "................................"
spotify_client_secret = "............................"
spotify_uri = "http://example.com"
spotify_user_id = '.................................'
spotify_scope = "playlist-modify-private"
spotify_playlist_id_one = '1dkTH9Uo5hNbvsFCkqjsHN'
spotify_playlist_id_two = "0XHmWJgxSNcVAUxVHsYUUB"

# ------------------------------------------------------------------------------------------------------------------#



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri=spotify_uri,
                                               scope=spotify_scope,
                                               show_dialog=True,
                                               cache_path=".cache"))

# -------------------------------------------------- To get the spotify username--------------------------------------#
# output= sp.current_user()
# print(output)
# ---------------------------------------------------Main code-------------------------------------------------#

spotify_uri_codes = []
spotify_track_codes  = []

for song in billboard_songs:
    spotify_songs = sp.search(q=f"track:{song} year:{amended_year}", market="US", offset=0 , limit=1)
    for selection in spotify_songs ['tracks'] ['items']:

        spotify_tracks = selection ['external_urls'] ['spotify']
        spotify_track_codes.append(spotify_tracks)

        spotify_uri = selection['uri']
        spotify_uri_codes.append(spotify_uri)

# print(spotify_track_codes)
# print(spotify_uri_codes)
billboard_top_100 = sp.user_playlist_create(user=spotify_user_id, name=f"{amended_date}Billboard 100", public=False)
# print(spotify_playlist)
add_songs= sp.playlist_add_items(playlist_id=spotify_playlist_id_two, items=spotify_uri_codes)
# print(add_songs)
