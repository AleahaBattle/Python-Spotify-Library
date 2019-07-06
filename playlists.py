import spotipy
import spotipy.util as util
import json
from json.decoder import JSONDecodeError
import os
import sys

# shows a user's playlists (need to be authenticated via oauth)

# Get tracks for user playlist
def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print(f" {i}, {track['artists'][0]['name']}, {track['name']}")

# run
if __name__ == '__main__':

    # Get the username id from terminal
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print('Whoops, need your username!')
        print(f'Usage: python user_playlists.py [username]')
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

        # User playlists
        playlists = spotify.user_playlists(username)
        # Get user playlists' name, total tracks, track info
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print(playlist['name'])
                print(f"Total Tracks: {playlist['tracks']['total']}")
                # Get playlist of user
                results = spotify.user_playlist(username, playlist['id'],
                    fields='tracks,next')
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = spotify.next(tracks)
                    show_tracks(tracks)
    else:
        print('Cannot get token for', username)
