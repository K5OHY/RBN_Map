import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Define the path to the spotters.csv file
spotters_csv_path = 'spotters.csv'

# Function to convert Maidenhead grid to latitude and longitude
def maidenhead_to_latlon(grid):
    if len(grid) < 4:
        raise ValueError("Grid square too short")
    grid = grid[:4].upper()
    lon = (ord(grid[0]) - ord('A')) * 20 - 180 + int(grid[2]) * 2 + 1
    lat = (ord(grid[1]) - ord('A')) * 10 - 90 + int(grid[3]) * 1 + 0.5
    return lat, lon

# Step 1: Scrape the RBN website
url = 'https://www.reversebeacon.net/nodes/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract table data
table = soup.find('table')
rows = table.find_all('tr')

# Collect spotters' data
spotters_data = []
for row in rows[1:]:  # Skip header row
    cols = row.find_all('td')
    if len(cols) >= 4:
        callsign = cols[0].text.strip()
        gridsquare = cols[3].text.strip()
        if gridsquare:
            spotters_data.append((callsign, gridsquare))

# Step 2: Convert grid squares to latitude and longitude
updated_data = []
for callsign, gridsquare in spotters_data:
    try:
        lat, lon = maidenhead_to_latlon(gridsquare)
        updated_data.append((callsign, lat, lon))
    except ValueError:
        updated_data.append((callsign, None, None))

# Step 3: Update the spotters.csv file
if os.path.exists(spotters_csv_path):
    spotters_df = pd.read_csv(spotters_csv_path)

    # Create a DataFrame from the updated data
    updated_df = pd.DataFrame(updated_data, columns=['callsign', 'latitude', 'longitude'])

    # Merge the data
    merged_df = spotters_df.merge(updated_df, on='callsign', suffixes=('_old', ''))
    merged_df['latitude'] = merged_df['latitude'].combine_first(merged_df['latitude_old'])
    merged_df['longitude'] = merged_df['longitude'].combine_first(merged_df['longitude_old'])
    merged_df = merged_df.drop(columns=['latitude_old', 'longitude_old'])

    # Save the updated spotters.csv
    merged_df.to_csv(spotters_csv_path, index=False)
    print("Spotters.csv updated successfully.")
else:
    print(f"Error: {spotters_csv_path} not found.")
