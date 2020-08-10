######## Goal of this project: ########
##  Communicate with Spotify API to learn about my own listening patterns

######## Steps to take ########
## Import Dependencies
## Authorize API call, change scope each time if necessary
## Grab last 50 played tracks with pertinent data
## Find new music based on Spotify's algorithm and your listening habits

##Export to CSV
##Figure out how to do this for more than only 50 lines

import spotipy.util as util
import spotipy
import requests
import pprint
import pandas as pd
pp=pprint.PrettyPrinter(indent=4)

#Client Credentials Flow via OAuth
username = 'mrprofessorchedog1891'
client_id = "52c92257dc74437daa506160fbd78e20"
client_secret = "226904b21e4249aea04da125b3ffd372"
redirect_uri = "http://localhost:7777/callback"
scope = "user-read-recently-played"
token = util.prompt_for_user_token(username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

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
new_artist_suggestions_by_song=[]
# [0]['name']
if token:
    sp = spotipy.Spotify(auth=token)
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
        print(entry)
        related_artists = sp.artist_related_artists(str(entry))['artists']
        for item in related_artists:
            new_artist_suggestions_by_artist.append(item['name'])
            for item in related_artists:
                new_artist_suggestions.append(item['name'])

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

MyMusicDF
##Full list of unique suggested artists for each artist_id
artists_to_try=set(new_artist_suggestions)
artists_to_try

##Full list of suggested artists for each song_id
MyMusicDF.to_csv("RecentlyPlayed.csv", sep=',')
