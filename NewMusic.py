######## Goal of this project: ########
##  Communicate with Spotify API to learn about my own listening patterns

######## Steps to take ########
## Import Dependencies
## Authorize API call, change scope each time if necessary
## Grab last 50 played tracks with pertinent data
## Find new music based on Spotify's algorithm and your recently played songs
## Create new playlist based on new recommended artists and Save playlist to my own Spotify account

##Export to CSV

import spotipy.util as util
import spotipy
import requests
import pprint
import pandas as pd
from datetime import date
pp=pprint.PrettyPrinter(indent=4)

#Client Credentials Flow via OAuth
username = 'mrprofessorchedog1891'
client_id = "52c92257dc74437daa506160fbd78e20"
client_secret = "226904b21e4249aea04da125b3ffd372"
redirect_uri = "http://localhost:7777/callback"
scope = "playlist-modify-public user-library-read playlist-modify-private playlist-read-private user-library-modify playlist-modify ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing streaming app-remote-control user-read-email user-read-private user-library-read user-top-read user-read-playback-position user-read-recently-played user-follow-read user-follow-modify"
token = util.prompt_for_user_token(username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)
#Create empty lists to hold your data
artists=[]
songs=[]
ids=[]
timestamp=[]
album_art = []
song_duration = []
popularity=[]
release_date=[]
artist_ids=[]
new_artist_suggestions_by_artist=[]
new_songs_for_playlist=[]

# Save data from API endpoints into your empty lists
if token:
    sp=spotipy.Spotify(auth=token)
    recently_played = sp.current_user_recently_played(limit=50)
    for item in recently_played['items']:
        song_duration.append(item['track']["duration_ms"])
        songs.append(item['track']['name'])
        album_art.append(item['track']["album"]['images'][0]['url'])
        ids.append(item['track']['id'])
        artists.append(item['track']['artists'][0]['name'])
        popularity.append(item['track']['popularity'])
        release_date.append(item['track']['album']['release_date'])
        artist_ids.append(item['track']['artists'][0]['id'])
    for entry in artist_ids:
        related_artists = sp.artist_related_artists(str(entry))['artists']
        for item in related_artists:
            related_ids.append(item['id'])
            new_artist_suggestions_by_artist.append(item['name'])


related_tracks=[]
# Turn lists into DF
MyMusicDF = pd.DataFrame({
"Songs":songs,
"Artists":artists,
"song_id": ids,
"artist_id":artist_ids,
"Release_Date":release_date,
"Album_Art":album_art,
"Popularity":popularity,
"Song_Duration (ms)":song_duration
})

##Full list of unique suggested artists for each artist_id
artists_to_try=set(new_artist_suggestions_by_artist)
new_songs_for_playlist=[]

## For each artist in artists_to_try, their top song to a playlist
for name in artists_to_try:
    new_songs_for_playlist.append(sp.search(q=name, limit=1, type='track')['tracks']['items'][0]['id'])
new_songs = new_songs_for_playlist[:100]
time = date.today().strftime("%d/%m/%Y")
new_playlist_id = sp.user_playlist_create(user=username, name=f"Scraped {time}", public=True, description= "I scraped my own Spotify API data to generate this playlist based off artists related to my recently played music")['id']
sp.user_playlist_add_tracks(user=username, playlist_id = new_playlist_id, tracks = new_songs)

##Full list of suggested artists for each song_id
MyMusicDF.to_csv("RecentlyPlayed.csv", sep=',')
