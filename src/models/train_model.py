from sklearn.naive_bayes import GaussianNB
import pandas as pd

def train_NB_model(trackset, training_set):
  useful_features = ['acousticness','danceability','instrumentalness','energy','speechiness','tempo','valence']
  X = training_set[useful_features]
  Y = training_set.status
  w = training_set.weight
  clf = GaussianNB()
  clf.fit(X, Y, sample_weight=w)
  predicts = pd.DataFrame(clf.predict_proba(trackset[useful_features]))
  predicts.columns = ['P_reject','P_accept']
  trackset.P_accept = predicts['P_accept'].values
  return trackset.sort_values(by=['P_accept'], ascending=False)