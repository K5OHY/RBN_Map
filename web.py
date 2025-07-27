
import requests
import pandas as pd
import folium
import matplotlib.colors as mcolors
import zipfile
import os
import re
from io import BytesIO
import streamlit as st
from datetime import datetime, timedelta, timezone, time
from geopy.distance import geodesic
import numpy as np
import math

from geographiclib.geodesic import Geodesic

DEFAULT_GRID_SQUARE = "DM81wx"  # Default grid square location

def download_and_extract_rbn_data(date):
    url = f'https://data.reversebeacon.net/rbn_history/{date}.zip'
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            csv_filename = None
            for file_info in z.infolist():
                if file_info.filename.endswith('.csv'):
                    csv_filename = file_info.filename
                    z.extract(csv_filename)
                    break
            if csv_filename is None:
                raise Exception("No CSV file found in the ZIP archive")
            return csv_filename
    else:
        raise Exception(f"Error downloading RBN data: {response.status_code}")

def get_color(snr):
    color_map = mcolors.LinearSegmentedColormap.from_list('custom', ['green', 'yellow', 'red'])
    return mcolors.to_hex(color_map(snr / 30))

def get_band(freq):
    try:
        freq = float(freq)
    except ValueError:
        return 'unknown'
    
    if 1800 <= freq <= 2000:
        return '160m'
    elif 3500 <= freq <= 4000:
        return '80m'
    elif 7000 <= freq <= 7300:
        return '40m'
    elif 10100 <= freq <= 10150:
        return '30m'
    elif 14000 <= freq <= 14350:
        return '20m'
    elif 18068 <= freq <= 18168:
        return '17m'
    elif 21000 <= freq <= 21450:
        return '15m'
    elif 24890 <= freq <= 24990:
        return '12m'
    elif 28000 <= freq <= 29700:
        return '10m'
    elif 50000 <= freq <= 54000:
        return '6m'
    else:
        return 'unknown'

def calculate_initial_bearing(start_coords, end_coords):
    """Calculate the initial bearing from start_coords to end_coords."""
    lat1, lon1 = map(math.radians, start_coords)
    lat2, lon2 = map(math.radians, end_coords)
    
    delta_lon = lon2 - lon1
    y = math.sin(delta_lon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360  # Normalize to 0-360
    return bearing

def interpolate_great_circle(start_coords, end_coords, num_points=50):
    geod = Geodesic.WGS84
    line = geod.InverseLine(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
    points = []

    last_lon = None

    for i in range(num_points + 1):
        s = i * line.s13 / num_points
        pos = line.Position(s)
        lat = pos['lat2']
        lon = pos['lon2']

        # Normalize longitude to avoid antimeridian wrapping
        if last_lon is not None:
            delta = lon - last_lon
            if delta > 180:
                lon -= 360
            elif delta < -180:
                lon += 360
        last_lon = lon

        points.append((lat, lon))

    return points

# Normalize longitude to keep spotters and paths aligned visually
def normalize_lon(lon):
    """Normalize longitude to the range [-180, 180]"""
    return ((lon + 180) % 360) - 180

def create_map(filtered_df, spotter_coords, grid_square_coords, show_all_beacons, grid_square, use_band_column, callsign, stats):
    # Normalize longitude function
    def normalize_lon(lon):
        return ((lon + 180) % 360) - 180

    # Normalize all coordinates
    normalized_spotter_coords = {spotter: (lat, normalize_lon(lon)) for spotter, (lat, lon) in spotter_coords.items()}
    gs_lat, gs_lon = grid_square_coords
    normalized_grid_square_coords = (gs_lat, normalize_lon(gs_lon))

    # Create dual coordinates for all spotters and grid square
    dual_spotter_coords = {}
    for spotter, (lat, lon) in spotter_coords.items():
        normalized_lon_val = normalize_lon(lon)
        # Force dual plotting: original, normalized, and wrapped
        dual_spotter_coords[spotter] = [
            (lat, lon),  # Original (e.g., 140°E)
            (lat, normalized_lon_val - 360 if normalized_lon_val > 0 else normalized_lon_val + 360),  # Wrapped (e.g., -220°E)
            (lat, normalized_lon_val)  # Normalized (e.g., -220°E)
        ]

    dual_grid_square_coords = [
        (gs_lat, gs_lon),  # Original (e.g., -94.5°W)
        (gs_lat, normalize_lon(gs_lon) - 360 if normalize_lon(gs_lon) > 0 else normalize_lon(gs_lon) + 360),  # Wrapped
        normalized_grid_square_coords
    ]

    m = folium.Map(location=normalized_grid_square_coords, zoom_start=2)  # Wider initial view
    
    # Plot spotters on both sides
    if show_all_beacons:
        for spotter, coords_list in dual_spotter_coords.items():
            for coords in coords_list:
                folium.CircleMarker(
                    location=coords,
                    radius=1,
                    color='black',
                    fill=True,
                    fill_color='black',
                    popup=folium.Popup(f"Spotter: {spotter}", parse_html=True)
                ).add_to(m)
       
    # Plot RBN spots on both sides
    for _, row in filtered_df.iterrows():
        spotter = row['spotter']
        if spotter in dual_spotter_coords:
            coords_list = dual_spotter_coords[spotter]
            snr = row['snr']
            time = row['time']
            time_str = time.strftime("%H:%M")
            for coords in coords_list:
                folium.CircleMarker(
                    location=coords,
                    radius=snr / 2,
                    popup=f'Spotter: {spotter}<br>SNR: {snr} dB<br>Time: {time_str}',
                    color=get_color(snr),
                    fill=True,
                    fill_color=get_color(snr)
                ).add_to(m)

    # Plot grid square on both sides
    for coords in dual_grid_square_coords:
        folium.Marker(
            location=coords,
            icon=folium.Icon(icon='star', color='red'),
            popup=f'Your Location: {grid_square}'
        ).add_to(m)
    
    band_colors = {
        '160m': '#FFFF00', '80m': '#003300', '40m': '#FFA500', '30m': '#FF4500',
        '20m': '#0000FF', '17m': '#800080', '15m': '#696969', '12m': '#00FFFF',
        '10m': '#FF00FF', '6m': '#F5DEB3'
    }

    # Collect all coordinates for bounds
    all_coords = dual_grid_square_coords
    for coords_list in dual_spotter_coords.values():
        all_coords.extend(coords_list)
    for _, row in filtered_df.iterrows():
        spotter = row['spotter']
        if spotter in dual_spotter_coords:
            coords_list = dual_spotter_coords[spotter]
            for coords in coords_list:
                all_coords.append(coords)
    for points in [interpolate_great_circle(normalized_grid_square_coords, coords) for coords in normalized_spotter_coords.values()]:
        all_coords.extend(points)

    # Fit map bounds to include all coordinates
    if all_coords:
        m.fit_bounds(all_coords)

    # Plot lines using normalized coordinates
    for _, row in filtered_df.iterrows():
        spotter = row['spotter']
        if spotter in normalized_spotter_coords:
            coords = normalized_spotter_coords[spotter]
            if use_band_column:
                band = row['band']
            else:
                freq = row['freq']
                band = get_band(freq)
            color = band_colors.get(band, 'blue')
            curve_points = interpolate_great_circle(normalized_grid_square_coords, coords)
            folium.PolyLine(
                locations=curve_points,
                color=color,
                weight=2,
                opacity=0.7
            ).add_to(m)
    
    band_stats = "<br>".join([f"{band}: {count}" for band, count in stats['bands'].items()])
    stats_html = f'''
     <div style="position: absolute; top: 20px; right: 20px; width: 150px; height: auto; 
     border:1px solid grey; z-index:9999; font-size:10px; background-color:white; padding: 10px;">
     <b>Callsign: {callsign}</b><br>Total Spots: {stats['spots']}<br>
     Max Distance: {stats['max_distance']:.2f} mi<br>Max SNR: {stats['max_snr']} dB<br>
     Average SNR: {stats['avg_snr']:.2f} dB<br><b>Bands:</b><br>{band_stats}
     </div>
     '''
    m.get_root().html.add_child(folium.Element(stats_html))

    legend_html = '''
    <div style="position: absolute; top: 50%; transform: translateY(-50%); left: 20px; width: auto; max-width: 150px; height: auto; 
    border:1px solid grey; z-index:9999; font-size:10px; background-color:white; padding: 5px; word-wrap: break-word;">
    <b>Legend</b><br><table>
        <tr><td>160m</td><td><i class="fa fa-circle" style="color:#FFFF00"></i></td></tr>
        <tr><td>80m</td><td><i class="fa fa-circle" style="color:#003300"></i></td></tr>
        <tr><td>40m</td><td><i class="fa fa-circle" style="color:#FFA500"></i></td></tr>
        <tr><td>30m</td><td><i class="fa fa-circle" style="color:#FF4500"></i></td></tr>
        <tr><td>20m</td><td><i class="fa fa-circle" style="color:#0000FF"></i></td></tr>
        <tr><td>17m</td><td><i class="fa fa-circle" style="color:#800080"></i></td></tr>
        <tr><td>15m</td><td><i class="fa fa-circle" style="color:#696969"></i></td></tr>
        <tr><td>12m</td><td><i class="fa fa-circle" style="color:#00FFFF"></i></td></tr>
        <tr><td>10m</td><td><i class="fa fa-circle" style="color:#FF00FF"></i></td></tr>
        <tr><td>6m</td><td><i class="fa fa-circle" style="color:#F5DEB3"></i></td></tr>
    </table></div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    return m
# Rest of your functions (grid_square_to_latlon, process_pasted_data, etc.) remain unchanged
def grid_square_to_latlon(grid_square):
    upper_alpha = "ABCDEFGHIJKLMNOPQR"
    digits = "0123456789"
    lower_alpha = "abcdefghijklmnopqrstuvwx"

    grid_square = grid_square.upper()

    lon = -180 + (upper_alpha.index(grid_square[0]) * 20) + (digits.index(grid_square[2]) * 2)
    lat = -90 + (upper_alpha.index(grid_square[1]) * 10) + (digits.index(grid_square[3]) * 1)

    if len(grid_square) == 6:
        lon += (lower_alpha.index(grid_square[4].lower()) + 0.5) / 12
        lat += (lower_alpha.index(grid_square[5].lower()) + 0.5) / 24

    return lat, lon

def process_pasted_data(pasted_data):
    lines = pasted_data.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    data = []
    for line in lines:
        parts = line.split()
        if len(parts) < 14:
            print(f"Skipping incomplete row: {line}")
            continue
        
        spotter = parts[0]
        dx = parts[1]
        distance = parts[2] + ' ' + parts[3]
        freq = parts[4]
        mode = parts[5]
        type_ = parts[6]
        snr = parts[7] + ' ' + parts[8]
        speed = parts[9] + ' ' + parts[10]
        time_str = parts[11] + ' ' + parts[12] + ' ' + parts[13]
        
        try:
            time = datetime.strptime(time_str, "%H%Mz %d %b")
        except ValueError:
            time = None
        
        if all([spotter, dx, distance, freq, mode, type_, snr, speed, time]):
            data.append([spotter, dx, distance, freq, mode, type_, snr, speed, time])
    
    df = pd.DataFrame(data, columns=['spotter', 'dx', 'distance', 'freq', 'mode', 'type', 'snr', 'speed', 'time'])
    
    df['snr'] = df['snr'].str.split().str[0].astype(float)
    df['freq'] = df['freq'].astype(float)
    
    if 'band' not in df.columns:
        df['band'] = df['freq'].apply(get_band)
    
    return df

def process_downloaded_data(filename):
    df = pd.read_csv(filename)
    df = df.rename(columns={'callsign': 'spotter', 'dx': 'dx', 'db': 'snr', 'freq': 'freq', 'band': 'band', 'date': 'time'})
    df['snr'] = pd.to_numeric(df['snr'], errors='coerce')
    df['freq'] = pd.to_numeric(df['freq'], errors='coerce')
    df['time'] = pd.to_datetime(df['time'])
    return df

def calculate_statistics(filtered_df, grid_square_coords, spotter_coords):
    spots = len(filtered_df)
    avg_snr = filtered_df['snr'].mean()
    max_snr = filtered_df['snr'].max()
    bands = filtered_df['band'].value_counts().to_dict()
    
    max_distance = 0
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            spotter = row['spotter']
            if spotter in spotter_coords:
                coords = spotter_coords[spotter]
                distance = geodesic(grid_square_coords, coords).miles
                if distance > max_distance:
                    max_distance = distance
    
    return {
        'spots': spots,
        'avg_snr': avg_snr,
        'max_distance': max_distance,
        'max_snr': max_snr,
        'bands': bands
    }

def main():
    st.set_page_config(layout="wide", page_title="RBN Signal Mapper", page_icon=":radio:")

    # Center the title
    st.markdown("<h1 style='text-align: center;'>RBN Signal Mapper</h1>", unsafe_allow_html=True)

    if 'map_html' not in st.session_state:
        st.session_state.map_html = None
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = None

    with st.sidebar:
        st.header("Input Data")
        callsign = st.text_input("Enter Callsign:")
        grid_square = st.text_input("Enter Grid Square (optional):")
        show_all_beacons = st.checkbox("Show all reverse beacons")
        data_source = st.radio(
            "Select data source",
            ('Paste RBN data', 'Download RBN data by date')
        )

        if data_source == 'Paste RBN data':
            pasted_data = st.text_area("Paste RBN data here:")
        else:
            date = st.text_input("Enter the date (YYYYMMDD):")

        generate_map = st.button("Generate Map")

        band_colors = {
            '160m': '#FFFF00',  # yellow
            '80m': '#003300',   # dark green
            '40m': '#FFA500',   # orange
            '30m': '#FF4500',   # red
            '20m': '#0000FF',   # blue
            '17m': '#800080',   # purple
            '15m': '#696969',   # dim gray
            '12m': '#00FFFF',   # cyan
            '10m': '#FF00FF',   # magenta
            '6m': '#F5DEB3',    # wheat
        }
        band_options = ['All'] + list(band_colors.keys())
        selected_band = st.selectbox('Select Band', band_options)

        # Adding the time slider
        st.subheader("Filter by UTC Time")
        start_time, end_time = st.slider(
            "Select time range",
            value=(time(0, 0), time(23, 59)),
            format="HH:mm"
        )

        with st.expander("Instructions", expanded=False):
            st.markdown("""
            **Instructions:**
            1. Enter a callsign and grid square.
            2. Select the data source:
                - Paste RBN data manually.
                - Download RBN data by date.
            3. Optionally, choose to show all reverse beacons.
            4. Click 'Generate Map' to visualize the signal map.
            5. You can download the generated map using the provided download button.
            """)

    if generate_map:
        try:
            with st.spinner("Generating map..."):
                use_band_column = False
                file_date = ""

                if callsign:
                    callsign = callsign.upper()

                if grid_square:
                    grid_square = grid_square[:2].upper() + grid_square[2:]

                if not grid_square:
                    st.warning(f"No grid square provided, using default: {DEFAULT_GRID_SQUARE}")
                    grid_square = DEFAULT_GRID_SQUARE

                if data_source == 'Paste RBN data' and not pasted_data.strip():
                    data_source = 'Download RBN data by date'
                    date = ""

                if data_source == 'Paste RBN data' and pasted_data.strip():
                    df = process_pasted_data(pasted_data)
                    st.write("Using pasted data.")
                    file_date = datetime.now(timezone.utc).strftime("%Y%m%d")
                elif data_source == 'Download RBN data by date':
                    if not date.strip():
                        yesterday = datetime.now(timezone.utc) - timedelta(1)
                        date = yesterday.strftime('%Y%m%d')
                        st.write(f"Using latest available date: {date}")
                    csv_filename = download_and_extract_rbn_data(date)
                    df = process_downloaded_data(csv_filename)
                    os.remove(csv_filename)
                    use_band_column = True
                    file_date = date
                    st.write("Using downloaded data.")
                else:
                    st.error("Please provide the necessary data.")

                filtered_df = df[df['dx'] == callsign].copy()
                st.session_state.filtered_df = filtered_df.copy()  # Store the filtered dataframe in session state

                # Filter by the selected time range
                filtered_df = filtered_df[(filtered_df['time'].dt.time >= start_time) & (filtered_df['time'].dt.time <= end_time)]

                spotter_coords_df = pd.read_csv('spotter_coords.csv')
                spotter_coords = {
                    row['callsign']: (row['latitude'], row['longitude']) for _, row in spotter_coords_df.iterrows()
                }

                if grid_square:
                    grid_square_coords = grid_square_to_latlon(grid_square)
                else:
                    grid_square_coords = grid_square_to_latlon(DEFAULT_GRID_SQUARE)

                if selected_band != 'All':
                    filtered_df = filtered_df[filtered_df['band'] == selected_band]

                stats = calculate_statistics(filtered_df, grid_square_coords, spotter_coords)

                m = create_map(filtered_df, spotter_coords, grid_square_coords, show_all_beacons, grid_square, use_band_column, callsign, stats)
                map_html = m._repr_html_()
                st.session_state.map_html = map_html
                st.session_state.file_date = file_date
                st.write("Map generated successfully!")

                # Adding the download button within the same container
                st.download_button(
                    label="Download Map",
                    data=map_html,
                    file_name=f"RBN_signal_map_{file_date}.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"Error: {e}")

    elif st.session_state.filtered_df is not None:
        try:
            with st.spinner("Filtering data..."):
                filtered_df = st.session_state.filtered_df.copy()

                if selected_band != 'All':
                    filtered_df = filtered_df[filtered_df['band'] == selected_band]

                # Filter by the selected time range
                filtered_df = filtered_df[(filtered_df['time'].dt.time >= start_time) & (filtered_df['time'].dt.time <= end_time)]

                spotter_coords_df = pd.read_csv('spotter_coords.csv')
                spotter_coords = {
                    row['callsign']: (row['latitude'], row['longitude']) for _, row in spotter_coords_df.iterrows()
                }

                if grid_square:
                    grid_square_coords = grid_square_to_latlon(grid_square)
                else:
                    grid_square_coords = grid_square_to_latlon(DEFAULT_GRID_SQUARE)

                stats = calculate_statistics(filtered_df, grid_square_coords, spotter_coords)

                m = create_map(filtered_df, spotter_coords, grid_square_coords, show_all_beacons, grid_square, True, callsign, stats)
                map_html = m._repr_html_()
                st.session_state.map_html = map_html
                st.write("Data filtered successfully!")

                # Adding the download button within the same container
                st.download_button(
                    label="Download Map",
                    data=map_html,
                    file_name=f"RBN_signal_map_{st.session_state.file_date}.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.map_html:
        st.components.v1.html(st.session_state.map_html, height=700)

if __name__ == "__main__":
    main()
