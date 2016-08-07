import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import json


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
    results = sp.recommendations(seed_tracks=input_tracks, limit=quantity_to_return, country='GB')
    for i, track in enumerate(results['tracks']):
        results_df.loc[i] = [track['id'],track['name'],track['artists'][0]['name']]
    return results_df

# Returns dataframe of IDs, track names, artist names and features for input seed tracks (max 5)
def get_new_recs_and_feats(input_tracks,quantity_to_return):
    new_tracks_df = get_recommends_from_seed(input_tracks,quantity_to_return)
    new_tracks_df = new_tracks_df.merge(get_features_for_tracks(new_tracks_df['id']), on='id')
    new_tracks_df.loc[:,'status'] = np.zeros(quantity_to_return)
    new_tracks_df.loc[:,'weight'] = np.ones(quantity_to_return)
    new_tracks_df.loc[:,'P_accept'] = np.ones(quantity_to_return)
    return new_tracks_df

# Returns dataframe of IDs, track names and artists names from input list of IDs
def get_tracks_details(input_tracks):
    sp = spotipy.Spotify()
    results = sp.tracks(input_tracks)
    results_df = pd.DataFrame(columns=('id','track_name','artist_name'))
    for i, track in enumerate(results['tracks']):
        results_df.loc[i] = [track['id'],track['name'],track['artists'][0]['name']]
    return results_df

# Builds training set from initial seed and puts it into standardised dataframe.
def define_training_set(init_seed):
  training_set = get_tracks_details(init_seed).merge(get_features_for_tracks(init_seed), on='id')
  training_set.loc[:,'status'] = np.ones(len(init_seed))
  training_set.loc[:,'weight'] = np.ones(len(init_seed))
  training_set.loc[:,'P_accept'] = np.zeros(len(init_seed))
  return training_set

# Cap and floor BPMs
def band_BPMs(track_features_frame, min_BPM, max_BPM):
    track_features_frame.loc[:,'tempo'] = list(map(lambda x: x/2 if (x>max_BPM) else x*2 if (x<min_BPM) else x, track_features_frame.tempo))
    return track_features_frame

def process_track(suggest_set, training_set, id, choice):
  suggest_set.loc[id,'status'] = choice
  if len(training_set) > 0:
    training_set.loc[len(training_set)] = suggest_set.loc[id]
  else:
    training_set = suggest_set.loc[id]
  suggest_set = suggest_set.drop([id])
  return (suggest_set, training_set)

###############################################
# Legacy function from initial data exploration
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

