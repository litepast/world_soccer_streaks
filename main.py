import pandas as pd
from streaks_w_pandas import Streak as Streak_pandas
import json
import time
import kaggle
from dotenv import load_dotenv

def download_data():
    load_dotenv('config.env')
    kaggle.api.authenticate()
    kaggle.api.dataset_metadata("patateriedata/all-international-football-results",path=".")
    kaggle.api.dataset_download_files("patateriedata/all-international-football-results",path=".",unzip=True)

def load_matches():    
    df = pd.read_csv("all_matches.csv")
    return df

def load_countries():
    df = pd.read_csv("countries_names.csv")
    df = df.loc[(df['original_name'] == df['current_name']) ]
    current_countries = df['original_name'].values.tolist()
    return current_countries

if __name__ == '__main__':
    test = True
    st = time.time()
    if not test:
        download_data()
    matches = load_matches()
    countries = load_countries()
    elapsed_time = time.time() - st
    print('E time', elapsed_time, 'seconds')


    st = time.time()
    streak_pd = Streak_pandas(matches, countries)
    top_streaks = streak_pd.get_all_top_streaks()
    active_streaks = streak_pd.get_all_active_streaks()
    json.dump(top_streaks, open('streaks_alltime.json', 'w'), indent=4)
    json.dump(active_streaks, open('streaks_active.json', 'w'), indent=4) 
    elapsed_time = time.time() - st
    print('TL time', elapsed_time, 'seconds')