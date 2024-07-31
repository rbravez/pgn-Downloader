import urllib.request  # Import the library to handle HTTP requests
import json  # Import the library to parse JSON data
import os  # Import the library for interacting with the operating system (file operations)
import pandas as pd  # Import the pandas library, though it is not used in the code
import time  # Import the library to introduce delays in execution
from datetime import datetime  # Import the datetime module to work with dates and times

# Function to download chess games for a specified user within a given date range
def download_chess_games(username, save_directory, start_year, start_month, end_year, end_month):
    # Base URL for the Chess.com API, specific to the user
    base_url = f"https://api.chess.com/pub/player/{username}/games/"
    # URL to fetch the list of available archives (monthly game collections)
    archives_url = base_url + "archives"
    # Headers to mimic a real browser request to avoid being blocked by the server
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Attempt to fetch the list of archives from Chess.com
    try:
        request = urllib.request.Request(archives_url, headers=headers)  # Create a request object with headers
        response = urllib.request.urlopen(request)  # Send the request and get the response
        data = json.loads(response.read().decode("utf-8"))  # Decode the JSON response to a Python dictionary
        archives_list = data['archives']  # Extract the list of archive URLs
    except Exception as e:
        # If there's an error (e.g., network issue), print the error message and exit the function
        print(f"Failed to retrieve archives: {e}")
        return
    
    # List to store filtered archive URLs based on the date range
    filtered_archives = []
    # Loop through the list of archive URLs
    for url in archives_list:
        # Extract the year and month from the URL
        year_month = url.split('/')[-2:]
        if len(year_month) == 2:
            year, month = map(int, year_month)
            # Check if the archive falls within the specified date range
            if (start_year < year < end_year) or \
               (year == start_year and month >= start_month) or \
               (year == end_year and month <= end_month):
                filtered_archives.append(url)  # Add the URL to the filtered list
    
    # List to store all games downloaded from the filtered archives
    all_games = []
    # Loop through the filtered archive URLs to download games
    for archive_url in filtered_archives:
        try:
            # Modify the archive URL to exclude time between moves (if desired)
            archive_url += "?clocks=false"
            request = urllib.request.Request(archive_url, headers=headers)  # Create a request object with headers
            response = urllib.request.urlopen(request)  # Send the request and get the response
            data = json.loads(response.read().decode("utf-8"))  # Decode the JSON response to a Python dictionary
            games = data['games']  # Extract the list of games
            all_games.extend(games)  # Add the games to the list of all games
            print(f"Retrieved {len(games)} games from {archive_url}")
            time.sleep(1)  # Wait for 1 second before the next request to avoid overloading the server
        except Exception as e:
            # If there's an error (e.g., network issue), print the error message and continue to the next archive
            print(f"Failed to retrieve games from {archive_url}: {e}")
    
    # If games were successfully retrieved, save them to a PGN file
    if all_games:
        # Create the full path for the output file
        filename = os.path.join(save_directory, f"{username}_games.pgn")
        save_to_pgn(all_games, filename)  # Call the function to save games to the file
        print(f"Saved {len(all_games)} games to {filename}")

# Function to save the list of games to a PGN file
def save_to_pgn(games, filename):
    # Open the file in write mode
    with open(filename, 'w') as f:
        # Loop through each game in the list
        for game in games:
            f.write(game['pgn'])  # Write the PGN data to the file
            f.write('\n\n')  # Add a newline after each game for readability
    print(f"Saved {len(games)} games to {filename}")

# Main execution block, executed when the script is run directly
if __name__ == "__main__":
    # Specify the Chess.com username whose games you want to download
    username = "name_of_player"  # Replace with desired username
    # Specify the directory where the games will be saved
    save_directory = r"Path"  # Replace with your desired directory
    # Define the start and end of the date range for the games to download
    start_year = 2022  # Specify the start year
    start_month = 1    # Specify the start month (1 = January, 12 = December)
    end_year = 2024    # Specify the end year
    end_month = 7      # Specify the end month (1 = January, 12 = December)
    
    # Check if the save directory exists, and create it if it doesn't
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Call the function to download the games within the specified date range
    download_chess_games(username, save_directory, start_year, start_month, end_year, end_month)
