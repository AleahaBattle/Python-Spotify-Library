import spotipy
import spotipy.util as util
import json
from json.decoder import JSONDecodeError
import os
import sys


# Get the username id from terminal
if len(sys.argv) > 3:
    username = sys.argv[1]
    playlist_id = sys.argv[2]
    track_ids = sys.argv[3]
else:
    print(f'Usage: {sys.argv[0]} username playlist_id track_id...')
    sys.exit()

# Add scope
scope = 'playlist-modify-public user-modify-playback-state'

# Erase cache and get user's permission to run app
try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f'.cache-{username}')
    token = util.prompt_for_user_token(username, scope)

if token:
    # Spotify object
    spotify = spotipy.Spotify(auth=token)
    # Turn off tracing
    spotify.trace = False
    # Add tracks to a playlist
    results = spotify.user_playlist_add_tracks(username, playlist_id, track_ids)
    print(results)
else:
    print('Cannot get token for', username)
