import json
from geopy.geocoders import Nominatim
import csv

# Create a Nominatim geocoder instance
geolocator = Nominatim(user_agent="reverse_geocoding")

# Load the JSON file with coordinates and date visited (Records.json)
with open('/path/to/Records.json', 'r') as json_file:
    data = json.load(json_file)

location_list = []

# Iterate through the locations
for entry in data['locations']:
    if 'latitudeE7' in entry and 'longitudeE7' in entry:
        lat = entry['latitudeE7'] / 1e7  # Convert latitudeE7 to decimal degrees
        lng = entry['longitudeE7'] / 1e7  # Convert longitudeE7 to decimal degrees
        date_visited = entry.get('timestamp', 'Date Unknown')
        location = geolocator.reverse((lat, lng), exactly_one=True)

        if location:
            location_name = location.raw.get('display_name', 'Unknown Location')
            location_list.append([date_visited, location_name])
    else:
        print(f"Skipping entry due to missing latitudeE7 or longitudeE7: {entry}")

# Write the results to a CSV file (visited_locations.csv)
with open('/path/to/visited_locations.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Date Visited', 'Location Name'])
    csv_writer.writerows(location_list)

print("Results have been written to 'visited_locations.csv'")
