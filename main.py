"""
Main module to get all streaks for world streaks website
"""

import json
import os
import requests
from base64 import b64encode
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

def commit_to_github(streaks_data):
    github_token =  os.getenv("GITHUB_KEY")
    repo_owner = "litepast"
    repo_name = "world_soccer_streaks"
    file_path = "streaks_fe/src/data/streaks.json"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers =  headers={"Authorization": f"token {github_token}"}
    commit_message = "Updated file from Weekly Update"

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        current_sha = response.json()["sha"]
    else:
        return {'status': response.status_code, 'message': 'No sha'}

    payload = {
        "message": commit_message,
        "content": str(b64encode(bytes(json.dumps(streaks_data, indent=4), 'utf-8')), 'utf-8'),
        "branch": "main"
    }

    if current_sha:
        payload["sha"] = current_sha

    response = requests.put(api_url, headers=headers, json=payload)
    success_msg = response.json()["commit"]["message"]

    if response.status_code == 200:
        return {'status': response.status_code, 'message': success_msg}
    else:
        return {'status': response.status_code, 'message': 'Error'}


if __name__ == '__main__':
    try:
        load_dotenv('config.env')
        JSON_DIR = './streaks_fe/src/data/streaks.json'
        download_data()
        matches = load_matches()
        countries = load_countries()
        streaks = Streak(matches, countries)
        streaks_json = streaks.get_all_top_streaks()
        status = commit_to_github(streaks_json)
        json.dump(streaks_json, open(JSON_DIR, 'w', encoding="utf-8"), indent=4)
        print(status)
    except Exception as error:
        print("An exception occurred:", type(error).__name__)
