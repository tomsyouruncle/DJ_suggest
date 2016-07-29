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

def get_recommends_from_seed(input_tracks,quantity_to_return):
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = False
    results_dict = {'id':[],'track_name':[],'artist_name':[]}
    results = sp.recommendations(seed_tracks=input_tracks, limit=quantity_to_return, country=None)
    for track in results['tracks']:
        # results_array.append(track['id'])
        results_dict['id'].append(track['id'])
        results_dict['track_name'].append(track['name'])
        results_dict['artist_name'].append(track['artists'][0]['name'])
    return results_dict

def get_new_recs_and_feats(input_tracks,quantity_to_return):
    new_tracks_dict = get_recommends_from_seed(input_tracks,quantity_to_return)
    new_trackset_df = features_list(new_tracks_dict['id'])
    new_trackset_df['track_name'] = new_tracks_dict['track_name']
    new_trackset_df['artist_name'] = new_tracks_dict['artist_name']
    return new_trackset_df


def band_BPMs(track_features_frame, min_BPM, max_BPM):
    track_features_frame.tempo = list(map(lambda x: x/2 if (x>max_BPM) else x*2 if (x<min_BPM) else x, track_features_frame.tempo))
    return track_features_frame

def split_head_tail(df, head_size):
    head_df = df.head(head_size)
    tail_df = df.tail(df.shape[0] - head_size)
    return [head_df, tail_df]

