# Network Traffic Visualization Tool

The purpose of this project is to develop a network traffic visualization tool that integrates Wireshark for packet capture, Python for data processing, and Google Maps for visualization by extracting source and destination IP addresses from `.pcap` files. It integrates the **Scapy** library to extract source and destination IP from packets, **PyGeoIP** To map IP addresses to geographical locations coordinates, and generates a **KML** file to visualize the traffic on **Google Maps**.

The tool identifies the geographical locations of IP addresses and color-codes traffic paths based on the continent. It is useful for network analysts, incident responders, and security professionals to analyze network traffic, detect anomalies, and map geolocated network flows.

## Features

- **Packet Capture Parsing**: Reads `.pcap` and `.pcapng` files using Scapy.
- **Geo-location**: Maps IP addresses to their geographical locations using the **GeoLiteCity.dat** database.
- **KML Generation**: Generates a KML file for visualizing network traffic on Google Maps.
- **Continent-based Color Coding**: Uses different colors for network traffic based on the continent of the IP address (North America, South America, Europe, Asia, Africa, Oceania).

## Requirements

- Python 3.x
- **Scapy**: Used for parsing `.pcap` files.
- **PyGeoIP**: Used for IP geolocation based on the GeoLiteCity database.
- **EasyGui**: Used for opening a file dialog to select the `.pcap` file.
- **GeoLiteCity.dat**: A geolocation database for mapping IP addresses to geographical locations.

### Install Required Libraries

Install the required Python libraries with `pip` or `pip3`:

```bash
pip install scapy
pip install pygeoip
pip install easygui

Additionally, download the GeoLiteCity.dat file from MaxMind and place it in the same directory as the script.
How It Works

    Packet File Selection: The user selects a .pcap or .pcapng file through a file dialog.
    Packet Processing: The script processes the packets in the file, extracting source and destination IP addresses.
    Geolocation Lookup: For each IP address, the script uses the GeoLiteCity database to find the geographical location (latitude and longitude).
    KML Generation: The script generates a KML file containing the geolocated IP addresses and paths between them.
    Google Maps Visualization: The generated KML file can be uploaded to Google Maps for visualizing the traffic on a map.

Usage

1. Clone this repository to your local machine:
git clone https://github.com/your-username/network-traffic-visualization.git

2. Navigate to the directory where the script is located:
cd network-traffic-visualization

3. Ensure you have the GeoLiteCity.dat file in the same directory as the script.

4.Run the script:
python ntv.py

5. Select a .pcap or .pcapng file using the file dialog.

6. After processing, the script will save a KML file named kmlSample.kml in the same directory.

7. The script will open a Google Maps page in your default browser with the map of your network traffic.

Acknowledgments

    Scapy for packet manipulation and parsing.
    PyGeoIP for IP geolocation.
    EasyGui for creating the file selection dialog.
    MaxMind for the GeoLiteCity database.

Feel free to open an issue or pull request if you encounter any problems or have suggestions for improvements!
