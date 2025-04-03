"""
Main module to get all streaks for world streaks website
"""

import json
import pandas as pd
import kaggle
from dotenv import load_dotenv
from streak import Streak

def download_data():
    """Download Kaggle dataset"""
    load_dotenv('config.env')
    kaggle_dataset = "patateriedata/all-international-football-results"
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(kaggle_dataset,path=".",unzip=True,  quiet = True)

def load_matches():
    """Load matches dataset to pandas"""  
    df = pd.read_csv("all_matches.csv")
    return df

def load_countries():
    """Load current names dataset to pandas"""
    df = pd.read_csv("countries_names.csv")
    df = df.loc[(df['original_name'] == df['current_name']) ]
    current_countries = df['original_name'].values.tolist()
    return current_countries

if __name__ == '__main__':
    try:
        JSON_DIR = './streaks_fe/src/data/streaks.json'
        download_data()
        matches = load_matches()
        countries = load_countries()
        streaks = Streak(matches, countries)
        streaks_json = streaks.get_all_top_streaks()
        json.dump(streaks_json, open(JSON_DIR, 'w', encoding="utf-8"), indent=4)
        print('Ready')
    except Exception as error:
        print("An exception occurred:", type(error).__name__)
