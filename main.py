#This program will use billboard to find the best 100 songs for a date chosen by the user
#and then use spotify API to create a playlist with the 100 songs in the playlist.

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth
App_client='035bd363f60942318df114736fdc2f4f'
App_Secret='27c7f8d4cf174af597bfee60e543008b'
spotify_id='ahmadkhalifeh'
redirect_uri="http://localhost:8080/spotify/callback"


#inputting a date
date_input=input("what time would you like to travel back in time.Please type the date in format yyyy-mm-dd?\n")
#formatting the date
date_obj = datetime.strptime(date_input, "%Y-%m-%d")
year=date_input.split("-")[0]
print(date_obj)

#Creating a song list and using beautiful soup to format HTML content of billboard
song_list=[]
billboard_html_content=requests.get(url=f"https://www.billboard.com/charts/hot-100/{date_input}/")
billboard_response=BeautifulSoup(billboard_html_content.text, 'html.parser')

#Extracting song text from HTML
soup=billboard_response.select('li ul li h3')

#Adding extracting song to a list
for song in soup:
    new_song=song.get_text()
    new_song_text=new_song.strip()
    song_list.append(new_song_text)


pprint.pprint(song_list)

#Autehnticating users on Spotify using spotipy (not Oauth) and creating a spotify API Client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=App_client,
        client_secret=App_Secret,
        redirect_uri=redirect_uri,
        scope="playlist-modify-private",
        cache_path="token.txt",
        username='spotify_id',
        show_dialog=True,
    )
)


#Extracting the user_id
user_id=sp.current_user()["id"]
print(sp.current_user())
print(f"User ID: {user_id}")

#Creating a playlist on Spotify after authentication
playlist_id = sp.user_playlist_create(user=user_id, name=f"{date_input}Billboard 100", public=False)['id']

#Using the song uri to query an item and use its uri
song_uris=[]
for song in song_list:
    result=sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)

    if result['tracks']['items']:
        song_uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(song_uri)
    else:
        print(f"Song {song} not found on Spotify")

#printing the URI's
print(song_uris)

#Add items to the created playlist
if song_uris:
    sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
else:
    print("No playlist created, choose another date")
