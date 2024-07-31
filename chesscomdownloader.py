import urllib.request
import json
import os
import pandas as pd
import time
from datetime import datetime

def download_chess_games(username, save_directory, start_year, start_month, end_year, end_month):
    base_url = f"https://api.chess.com/pub/player/{username}/games/"
    archives_url = base_url + "archives"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Fetch the archives URL and parse JSON
    try:
        request = urllib.request.Request(archives_url, headers=headers)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode("utf-8"))
        archives_list = data['archives']
    except Exception as e:
        print(f"Failed to retrieve archives: {e}")
        return
    
    # Filter archives for the specified date range
    filtered_archives = []
    for url in archives_list:
        year_month = url.split('/')[-2:]
        if len(year_month) == 2:
            year, month = map(int, year_month)
            if (start_year < year < end_year) or \
               (year == start_year and month >= start_month) or \
               (year == end_year and month <= end_month):
                filtered_archives.append(url)
    
    all_games = []
    for archive_url in filtered_archives:
        try:
            archive_url += "?clocks=false"  # Exclude time between moves
            request = urllib.request.Request(archive_url, headers=headers)
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode("utf-8"))
            games = data['games']
            all_games.extend(games)
            print(f"Retrieved {len(games)} games from {archive_url}")
            time.sleep(1)  # Respectful delay to avoid overloading the server
        except Exception as e:
            print(f"Failed to retrieve games from {archive_url}: {e}")
    
    if all_games:
        filename = os.path.join(save_directory, f"{username}_games.pgn")
        save_to_pgn(all_games, filename)
        print(f"Saved {len(all_games)} games to {filename}")

def save_to_pgn(games, filename):
    with open(filename, 'w') as f:
        for game in games:
            f.write(game['pgn'])
            f.write('\n\n')
    print(f"Saved {len(games)} games to {filename}")

if __name__ == "__main__":
    username = "name_of_plater"  # Replace with desired username
    save_directory = r"path"  # Replace with your desired directory
    start_year = 2022  # Specify the start year
    start_month = 1    # Specify the start month (1 = January, 12 = December)
    end_year = 2024    # Specify the end year
    end_month = 7      # Specify the end month (1 = January, 12 = December)
    
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    download_chess_games(username, save_directory, start_year, start_month, end_year, end_month)
