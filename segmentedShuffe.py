import random

import spotipy

from spotipy.oauth2 import SpotifyOAuth


scope = "playlist-modify-private"

# Requires API keys (client_id, client_secret) as well as the playlist id, feed these by changing the empty strings or .env

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",client_secret="",scope=scope, redirect_uri=""))


# will divide all of the songs into segments, making it easy to count remaining songs in each segment and append them into
# a new list
segments = [[]]

user = sp.current_user()
user_id = user['id']

shuffled_songs = []




def process_tracks(items, segments):
    for idx, item in enumerate(items):
        track = item['track']
        track_id = track['id']
        segments[-1].append(track_id)


def generate_shuffle(segments, shuffled_songs):
    counter = 0
    while segments:
        random_segment = random.randint(0,len(segments)-1)
        current_selection = segments[random_segment]

        random_song = current_selection.pop(random.randint(0,len(current_selection)-1))
        counter +=1
        shuffled_songs.append(random_song)

        if not current_selection:
            segments.pop(random_segment)





playl = sp.playlist_items(playlist_id="")

playlist_info = sp.playlist(playlist_id="")

# Extract the name of the playlist from the playlist_info dictionary
playlist_name = playlist_info['name']

playlist_name = f"newly shuffled {playlist_name}"

new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

new_playlist_id = new_playlist['id']

process_tracks(playl['items'], segments)
next_counter = 1
while playl['next']:
    playl = sp.playlist_items(playlist_id="", offset=playl['offset'] + len(playl['items']))  # Fetch the next page of tracks
    segments.append([])
    process_tracks(playl['items'], segments)  # Process the tracks on the current page
    next_counter += 1

generate_shuffle(segments, shuffled_songs)


# Define the chunk size (e.g., 50 tracks per request)
chunk_size = 50

# Split the list of track IDs into chunks
track_id_chunks = [shuffled_songs[i:i + chunk_size] for i in range(0, len(shuffled_songs), chunk_size)]

# Add tracks to the playlist in chunks
for chunk in track_id_chunks:
    sp.playlist_add_items(playlist_id=new_playlist_id, items=chunk)
