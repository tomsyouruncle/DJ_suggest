import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
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

# Returns dataframe of IDs and features for each input track
def get_features_for_tracks(track_ids_array):
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    features = sp.audio_features(track_ids_array)
    return pd.read_json(json.dumps(features, indent=4))

# Returns dataframe of IDs, track names and artist names for recommendations
def get_recommends_from_seed(input_tracks,quantity_to_return): 
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    results_df = pd.DataFrame(columns=('id','track_name','artist_name'))
    results = sp.recommendations(seed_tracks=input_tracks, limit=quantity_to_return, country=None)
    for i, track in enumerate(results['tracks']):
        results_df.loc[i] = [track['id'],track['name'],track['artists'][0]['name']]
    return results_df

# Returns dataframe of IDs, track names, artist names and features for input seed tracks (max 5)
def get_new_recs_and_feats(input_tracks,quantity_to_return):
    new_tracks = get_recommends_from_seed(input_tracks,quantity_to_return)
    new_trackset_df = get_features_for_tracks(new_tracks['id'])
    new_trackset_df['track_name'] = new_tracks['track_name']
    new_trackset_df['artist_name'] = new_tracks['artist_name']
    new_trackset_df['state'] = np.zeros(quantity_to_return)
    return new_trackset_df

# Returns dataframe of IDs, track names and artists names from input list of IDs
def get_tracks_details(input_tracks):
    sp = spotipy.Spotify()
    results = sp.tracks(input_tracks)
    results_df = pd.DataFrame(columns=('id','track_name','artist_name'))
    for i, track in enumerate(results['tracks']):
        results_df.loc[i] = [track['id'],track['name'],track['artists'][0]['name']]
    return results_df

def band_BPMs(track_features_frame, min_BPM, max_BPM):
    track_features_frame.tempo = list(map(lambda x: x/2 if (x>max_BPM) else x*2 if (x<min_BPM) else x, track_features_frame.tempo))
    return track_features_frame

def split_head_tail(df, head_size):
    head_df = df.head(head_size)
    tail_df = df.tail(df.shape[0] - head_size)
    return [head_df, tail_df]

