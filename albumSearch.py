import spotipy
import spotipy.util as util
import webbrowser
import json
from json.decoder import JSONDecodeError
import os
import sys
from pprint import pprint

# Get the username id from terminal
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print(f'Usage: {sys.argv[0]} username')
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

    # Get a list of user’s available devices.
    # devices = spotify.devices()
    # device_id = devices['devices'][0]['id']

    # Get detailed profile information about the current user
    user = spotify.current_user()
    display_name = user['display_name']
    followers = user['followers']['total']

    while True:
        print(f'Welcome to Your Spotify Library {display_name}!')
        print(f'You have {followers} followers.')
        print('Menu:')
        print('s - Search for an an album')
        print('e - to Exit\n')
        choice = input('\nYour choice: ').lower()
        
        # Begin album Search
        if choice == 's':
            # Get search query
            query = input('\nEnter the name of the album: ')
            # Searches for an album
            results = spotify.search(query, 1, 0, 'album')
            
            # Album search results
            album_artist = input('\nEnter the name of the artist: ')
            try:
                album = results['albums']['items'][0]
                print(json.dumps(album, sort_keys=True, indent=4))
                name = album['name']
                release_year = album['release_date']
                total_tracks = album['total_tracks']
                print(name)
                print(f'Year album was realeased: {release_year}')
                print(f'Total tracks: {total_tracks}')
                webbrowser.open(album['images'][0]['url'])
                album_id = album['id']
            except:
                print(f'Album not found for {album_artist}')
        
        # Exit Loop
        if choice == 'e':
            break
    
    print('Goodbye!')
    

else:
    print('Cannot get token for', username)
            
# print(json.dumps(track_results, sort_keys=True, indent=4))



# export SPOTIPY_CLIENT_ID='<client_id>'
# export SPOTIPY_CLIENT_SECRET='<client_secret>'
# export SPOTIPY_REDIRECT_URI='http://127.0.0.1/callback'
# python3 spotify.py henryjune91

# export SPOTIPY_CLIENT_ID='07f7b44e246d418cb18d476a11a9ba92'
# export SPOTIPY_CLIENT_SECRET='502db2282f3d46df829209569a38fa62'

