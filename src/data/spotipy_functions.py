import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json

def get_tracks_from_playlist(username,p_id):  
    output_ids = [] 
    token = util.prompt_for_user_token(username)
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.user_playlist(username, p_id, fields="tracks,next")
        tracks = results['tracks']
        for i, item in enumerate(tracks['items']):
            track = item['track']
            output_ids.append(str(track['id']))
        return output_ids
    else:
        print("Can't get token for", username)

def features_list(track_ids_array):
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    features = sp.audio_features(track_ids_array)
    return pd.read_json(json.dumps(features, indent=4))

