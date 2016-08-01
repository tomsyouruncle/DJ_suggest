# import requests
from __future__ import print_function    # (at top of module)
import time
import sys
import os
import pandas as pd
import numpy as np
import pickle

PROJ_ROOT = os.path.join(os.getcwd(), os.pardir, os.pardir)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.display.float_format = '{:,.3f}'.format

# load environment variables from .env file using dotenv.
from dotenv import load_dotenv
dotenv_path = os.path.join(PROJ_ROOT, '.env')
load_dotenv(dotenv_path)

# add the 'src' directory as one where we can import modules
src_dir = os.path.join(PROJ_ROOT, 'src')
sys.path.append(src_dir)

from data.spotipy_functions import *
from models.train_model import *


def define_seed():
  print("Enter between 1 and 5 seed track spotify IDs")
  init_seed = []
  for i in range(5):
    inp = input("Enter track seed (ENTER for none): ")
    if inp == "":
      break
    else:
      init_seed.append(inp)
  return init_seed

#MAIN
init_seed = define_seed()
print("Generating recommendations...")
training_set = define_training_set(init_seed)
suggest_set = band_BPMs(get_new_recs_and_feats(init_seed,30),80,170)
gui_cols = ['artist_name','track_name','tempo','uri','status']
acc_rej = ''
while acc_rej != 'q':
  print(' ')
  print('TRAINING SET')
  print('------------')
  print(training_set[gui_cols])
  print(' ')
  print('RECOMMENDATIONS')
  print('---------------')
  print(suggest_set[gui_cols + ['P_accept']])
  print(' ')
  print('Type a# or r# to accept or reject a track.')
  print('(e.g. To accept track 5, type: a5)')
  print('To Save, type: s')
  print('To get new recommendations from a new seed, type: g')
  acc_rej = input('To quit, type: q   > ')
  if acc_rej[0] == 'a':
    suggest_set, training_set = process_track(suggest_set, training_set, int(acc_rej[1:]), 1)
  elif acc_rej[0] == 'r':
    suggest_set, training_set = process_track(suggest_set, training_set, int(acc_rej[1:]), -1)
  elif acc_rej == 'q':
    break
  elif acc_rej == 's':
    training_set.to_pickle(os.path.join(PROJ_ROOT,'data','interim','training_set.pkl'))
    suggest_set.to_pickle(os.path.join(PROJ_ROOT,'data','interim','track_set.pkl'))
  elif acc_rej == 'g':
    init_seed = define_seed()
    suggest_set = band_BPMs(get_new_recs_and_feats(init_seed,30),80,170)
  else:
    print('Error, invalid input.')

  # only train the model when it has positive and negative examples
  if training_set.status.min() < 0:
    suggest_set = train_NB_model(suggest_set, training_set)





