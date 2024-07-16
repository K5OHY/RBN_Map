# RBN Signal Mapper

## Overview

The RBN Signal Mapper is a web application that visualizes Reverse Beacon Network (RBN) data on an interactive map. This tool allows amateur radio operators to visualize the reception of their signals across the world based on RBN data.

## Features

- **Download RBN Data**: Fetch and visualize the latest RBN data by date.
- **Manual Data Input**: Paste custom RBN data for visualization.
- **Spotter Visualization**: Option to show all reverse beacons on the map.
- **Statistics Display**: View statistics such as total spots, max distance, max SNR, average SNR, and band breakdown.
- **Color-coded Bands**: Different bands are color-coded for easy identification on the map.
- **Interactive Map**: Generated maps are interactive and can be downloaded for offline viewing.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/K5OHY/RBN_Map.git
    cd RBN_Map
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Usage

1. **Enter Callsign**: Enter your callsign in the provided text box.
2. **Enter Grid Square (optional)**: Enter your grid square. If left blank, a default grid square will be used.
3. **Select Data Source**:
    - **Paste RBN Data**: Manually paste RBN data in the provided text area.
    - **Download RBN Data by Date**: Enter the date (YYYYMMDD) to download RBN data for that day.
4. **Show All Reverse Beacons (optional)**: Check this option to display all reverse beacons on the map.
5. **Generate Map**: Click the "Generate Map" button to create the map.
6. **Download Map**: Use the download button to save the generated map as an HTML file.

## Example

[Download Example Map](example_map.html)

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

## Acknowledgements

Special thanks to the developers and contributors of the following libraries:
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [GridTools](https://pypi.org/project/gridtools/)
- [Geopy](https://geopy.readthedocs.io/)

## Contact

For any questions or inquiries, please contact [your-email@example.com](mailto:haletd@gmail.com).

---

### Recent Updates

#### v1.1.0
- Enhanced legend alignment and statistics box.
- Added dynamic height adjustment for the statistics box.
- Improved error handling for incomplete data.

#### v1.0.0
- Initial release with basic RBN data visualization features.
