import spotipy
import spotipy.util as util
import webbrowser
import json
from json.decoder import JSONDecodeError
import requests
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

    # Get detailed profile information about the current user
    user = spotify.current_user()
    display_name = user['display_name']
    followers = user['followers']['total']

    while True:
        print(f'Welcome to Your Spotify Library {display_name}!')
        print(f'You have {followers} followers.')
        print('Menu:')
        print('s - Search for an artist')
        print('e - Exit\n')
        choice = input('\nYour choice: ').lower()
        
        if choice == 's':
            # Get search query
            query = input('\nEnter the name of the artist: ')
            # searches for an item
            results = spotify.search(query, 1, 0, 'artist')

            # Atrist info
            artist = results['artists']['items'][0]
            print(artist['name'])
            print(f"{artist['name']} has {artist['followers']['total']} followers")
            print(f"Genres: {artist['genres']}")
            webbrowser.open(artist['images'][0]['url'])
            artist_id = artist['id']

            # Store track details
            track_uris = []
            track_art_url = []
            track_nums = 1

            # Get Spotify catalog information about an artist’s albums
            albums = spotify.artist_albums(artist_id, album_type='album')
            album_results = albums['items']

            # Get artist’s album info
            for album in album_results:
                print(f"Album: {album['name']}")
                album_id = album['id']
                album_art = album['images'][0]['url']

                # Get Spotify catalog information about an album’s tracks
                tracks = spotify.album_tracks(album_id)
                track_results = tracks['items']
                
                # Print tracks
                for track in track_results:
                    print(f"{track_nums}: {track['name']}")

                    # Add track uri and art url to lists
                    track_uris.append(track['uri'])
                    track_art_url.append(album_art)
                    track_nums += 1

            # Show album art
            while True:
                # Get song name to add and play track
                track_num = input('Enter the song number to see the art and play the song (or 0 to exit): ')
                
                # Go back to main menu
                if track_num == '0':
                    break
                
                tracks = []
                # Add track to list
                tracks.append(track_uris[int(track_num)])

                # Get a list of user’s available devices.
                # This will only work for premium
                devices = spotify.devices()
                # pprint(devices)
                device_id = devices['devices'][1]['id']
                try:
                    # Start or resume user’s playback
                    spotify.start_playback(None, None, tracks)
                    webbrowser.open(track_art_url[int(track_num)])

                    # # Pause user’s playback
                    # spotify.pause_playback(device_id)

                    # # Skip user’s playback to next track
                    # spotify.next_track(device_id)

                    # # Skip user’s playback to previous track
                    # spotify.previous_track(device_id)  
                except:
                    print('Sorry, Premium is required to play songs.')
                    print('Please upgrade to Premium to play songs from the terminal.')
                finally:
                    break

        # Exit Loop
        if choice == 'e':
            break
    
    print('Goodbye!')
    

else:
    print('Cannot get token for', username)
