import spotipy
import spotipy.util as util
import json
from json.decoder import JSONDecodeError
import os
import sys


# Get the username and artist name from terminal
if len(sys.argv) > 2:
    username = sys.argv[1]
    artist_name = sys.argv[2]
else:
    print(f'Usage: {sys.argv[0]} username artist_name')
    sys.exit()

# Add scope
scope = 'user-read-private user-library-read user-read-playback-state user-modify-playback-state'

# Erase cache and get user's permission to run app
try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f'.cache-{username}')
    token = util.prompt_for_user_token(username, scope)

if token:
    # Spotify object
    spotify = spotipy.Spotify(auth=token)
    
    # Search for artist
    find_artist = spotify.search(artist_name, 1, 0, 'artist')
   
    # Atrist info
    artist = find_artist['artists']['items'][0]
    artist_uri = artist['uri']
    artist_id = artist['id']
    
    # Get Spotify catalog information about an artist’s albums
    results = spotify.artist_albums(artist_uri, album_type='album')
    albums = results['items']

    # Add artist’s albums to list
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    
    # Print all albums found
    for album in albums:
        print(album['name'])
else:
    print('Cannot get token for', username)