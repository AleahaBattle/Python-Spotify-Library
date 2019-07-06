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
    print('Whoops, need your username and the artist name!')
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
    
    # Get Spotify catalog information about an artist’s top 10 tracks by country
    results = spotify.artist_top_tracks(artist_uri)

    # Print track info
    for track in results['tracks'][:10]:
        print('track: ' + track['name'])
        print(f"song preview: {track['preview_url']}")
        print(f"cover art: {track['album']['images'][0]['url']}")
        print(f"song url:  {track['external_urls']['spotify']}\n")
else:
    print('Cannot get token for', username)