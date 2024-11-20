from scapy.all import rdpcap
import pygeoip
import easygui
import os
import webbrowser



# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to GeoLiteCity.dat
geoip_path = os.path.join(script_dir, 'GeoLiteCity.dat')

# Initialize the GeoIP database with the dynamically constructed path
if os.path.exists(geoip_path):
    gi = pygeoip.GeoIP(geoip_path)
else:
    print(f"GeoLiteCity.dat file not found in the script's directory: {geoip_path}")


# Dictionary to map country codes to continent colors
continent_colors = {
    'NA': '7FFF0000',  # North America - Blue
    'SA': '7F00FF00',  # South America - Green
    'EU': '7F0000FF',  # Europe - Red
    'AF': '7FFF7F00',  # Africa - Cyan
    'AS': '7F800080',  # Asia - Purple
    'OC': '7FFF7F00',  # Oceania - Yellow
    'default': '7F808080'  # Default - Gray
}

#funtion to get color for the continent
def get_continent_color(country_code):
    continent_map = {
        'US': 'NA',
        'CA': 'NA',
        'BR': 'SA',
        'AR': 'SA', 
        'FR': 'EU', 
        'DE': 'EU', 
        'NG': 'AF', 
        'ZA': 'AF', 
        'CN': 'AS', 
        'IN': 'AS', 
        'AU': 'OC', 
        'NZ': 'OC',
        'NP': 'AS'  
    }
    continent = continent_map.get(country_code, 'default')  # Default if country not mapped
    return continent_colors.get(continent, continent_colors['default'])  # Use gray if unknown

def retKML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name('205.250.188.221') 
     # using Static source IP for this proof of concept, otherwise the file would be too large for google maps to handle

 
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        
        # Get country code and determine line color
        country_code = dst['country_code']

        # Check if the destination IP belongs to North America (US or CA)
        if country_code != 'US':
            print(f"Detected outside IP: {dstip}")

        line_color = get_continent_color(country_code)
        
        # Build KML placemark structure
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<Style>\n'
            f'<LineStyle><color>{line_color}</color><width>3</width></LineStyle>\n'
            '</Style>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        ) % (dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except Exception as e:
      #  print(f"Error in retKML: {e}")
        return ''
    
def plotIPs(pcap):
    kmlPts = ''
    for pkt in pcap:
        try:
            if pkt.haslayer('IP'):  # Check if the packet has an IP layer
               # print("IP layer found in packet")  # Debug statement
                ip = pkt['IP']
                src = ip.src
                dst = ip.dst
                KML = retKML(dst, src)
               # if KML:
               #     print(f"KML generated for {dst}")  # Debug statement
                kmlPts += KML
        except Exception as e:
            print(f"Error processing packet: {e}")
            pass
    return kmlPts

def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Open file dialog with easygui and filter for .pcap and .pcapng files
    file_path = easygui.fileopenbox(
        title="Select a pcap file",
        filetypes=["*.pcap", "*.pcapng"]
    )

    # Check if the file was selected and has the correct extension
    if file_path and (file_path.endswith('.pcap') or file_path.endswith('.pcapng')):
        # Read the selected pcap file using Scapy
        pcap = rdpcap(file_path)
        print("PCAP file loaded successfully!")
    elif file_path is None:
        print("File selection was canceled.")
        return  # Exit if no file is selected
    else:
        print("No valid pcap file selected.")
        return  # Exit if the file is not valid

    # KML header
    kmlheader = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
        '<Document>\n'
    )
    
    # KML footer
    kmlfooter = '</Document>\n</kml>\n'
    
    # Combine header, KML points, and footer
    kmldoc = kmlheader + plotIPs(pcap) + kmlfooter

    # Construct the path to save the KML file in the same directory as the script
    kml_file_path = os.path.join(script_dir, 'kmlSample.kml')

    # Save the KML document to a file in the script's directory
    with open(kml_file_path, 'w') as kmlfile:
        kmlfile.write(kmldoc)

    print(f"KML file saved as '{kml_file_path}'.")
    
    # Open the Google Maps link directly in the default web browser
    google_maps_url = "https://www.google.com/maps/d/"
    print("Opening Google Maps in your browser...")
    webbrowser.open(google_maps_url)

# Ensure the script runs as expected
if __name__ == '__main__':
    main()
