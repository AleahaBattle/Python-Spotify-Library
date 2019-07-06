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
        print('s - Search for a playlist')
        print('e - to Exit\n')
        choice = input('\nYour choice: ').lower()
        
        if choice == 's':
            # Get search query
            query = input('\nEnter the name of the playlist: ')
            # Searches for an album
            results = spotify.search(query, 1, 0, 'playlist')
            
             # Playlist search results
            print(json.dumps(results['playlists']['items'][0], sort_keys=True, indent=4))
            # playist = results['playlists']['items'][0]
            # print(playist['name'])
            # print(f"{playist['followers']['total']} followers")
            # print(f"Genres: {playist['genres'][0]}")
            # webbrowser.open(playist['images'][0]['url'])
            # playist_id = artist['id']

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

