import requests
from bs4 import BeautifulSoup
import csv

def gridsquare_to_latlon(gridsquare):
    """
    Convert a 6-character Maidenhead gridsquare to latitude and longitude.
    Returns (latitude, longitude) as floats representing the center of the gridsquare.
    """
    if len(gridsquare) != 6:
        raise ValueError("Gridsquare must be 6 characters")
    gridsquare = gridsquare.upper()
    A = gridsquare[0]
    B = gridsquare[1]
    C = gridsquare[2]
    D = gridsquare[3]
    E = gridsquare[4]
    F = gridsquare[5]
    if not (A.isalpha() and B.isalpha() and C.isdigit() and D.isdigit() and E.isalpha() and F.isalpha()):
        raise ValueError("Invalid gridsquare format")
    long_min = (ord(A) - ord('A')) * 20 - 180
    lat_min = (ord(B) - ord('A')) * 10 - 90
    long_square_min = long_min + int(C) * 2
    lat_square_min = lat_min + int(D) * 1
    long_subsquare_min = long_square_min + (ord(E) - ord('A')) * (1/12)
    lat_subsquare_min = lat_square_min + (ord(F) - ord('A')) * (1/24)
    center_long = long_subsquare_min + (1/24)
    center_lat = lat_subsquare_min + (1/48)
    return center_lat, center_long

# URL of the RBN nodes page
url = 'https://www.reversebeacon.net/nodes/'

# Fetch the webpage
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch the page")
    exit()

# Parse the HTML
html = response.text
soup = BeautifulSoup(html, 'html.parser')

# Find the table
table = soup.find('table')
if not table:
    print("No table found on the page")
    exit()

# Get all rows
rows = table.find_all('tr')
if len(rows) < 2:
    print("Table has no data rows")
    exit()

# Verify table structure
header = rows[0]
header_cells = header.find_all('th')
if len(header_cells) < 3 or header_cells[0].text.strip().lower() != 'callsign' or header_cells[2].text.strip().lower() != 'grid':
    print("Table structure unexpected")
    exit()

# Write to CSV
with open('rbn_nodes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['callsign', 'latitude', 'longitude'])
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) < 3:
            continue
        callsign = cells[0].find('a').text.strip() if cells[0].find('a') else cells[0].text.strip()
        gridsquare = cells[2].text.strip()
        try:
            lat, lon = gridsquare_to_latlon(gridsquare)
            writer.writerow([callsign, lat, lon])
        except Exception as e:
            print(f"Error processing {callsign}: {e}")
