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
        print('s - Search for a song')
        print('e - Exit\n')
        choice = input('\nYour choice: ').lower()
        
        if choice == 's':
            # Get search query
            query = input('\nEnter the name of the song: ')
            # searches for an item
            results = spotify.search(str(query), 1, 0, str(search_type))

            # Track search results
            # song_artist = input('\nEnter the name of the artist: ')
            try:
                # print(json.dumps(results['tracks']['items'][0], sort_keys=True, indent=4))
                # if results['tracks']['items'][0]['album']['artists']['name'].lower() == song_artist.lower():
                    song = results['tracks']['items'][0]
                    song_name = song['name']
                    album_name = song['album']['name']
                    # for i, artist in song['artists']:
                    #     song_artists = [name for artist in song['artists'][i]['name']]
                    release_year = song['album']['release_date']
                    disc = song['disc_number']
                    track_num = song['track_number']
                    duration = (song['duration'] / 1000) / 60
                    if song['explicit'] == 'true':
                        explicit = 'Yes'
                    else:
                        explicit = 'No'
                    print(f'{song_name} is on the album: {album_name}')
                    print(f'Year album was realeased: {release_year}')
                    print(f'{song_name} is on disc {disc}, track number {track_num}')
                    print(f'{song_name} is {duration} long')
                    print(f'Is {song_name} explicit? {explicit}')
                    webbrowser.open(song['images'][0]['url'])
                    song_id = song['id']
                # else:
                #     print(f'Song not found for {song_artist}.')
                except:
                    print(f'Song not found.')
            else:
                continue

        
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

