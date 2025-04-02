import pandas as pd
from streak import Streak
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
    streaks = Streak(matches, countries)
    streaks_json = streaks.get_all_top_streaks()
    ##json.dump(streaks_json, open('streaks.json', 'w'), indent=4)
    json.dump(streaks_json, open('./streaks_fe/src/data/streaks.json', 'w'), indent=4)
    elapsed_time = time.time() - st
    print('TL time', elapsed_time, 'seconds')