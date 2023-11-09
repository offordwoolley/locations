import json
from geopy.geocoders import Nominatim
import csv
from datetime import datetime

# Create a Nominatim geocoder instance
geolocator = Nominatim(user_agent="reverse_geocoding")

# Set the chunk size to control how many entries are processed at a time
chunk_size = 100

# Load the JSON file with coordinates and date visited (Records.json)
with open('Records.json', 'r') as json_file:
    data = json.load(json_file)

location_list = []

# Process the data in smaller chunks
for chunk_start in range(0, len(data['locations']), chunk_size):
    chunk_end = chunk_start + chunk_size
    chunk = data['locations'][chunk_start:chunk_end]

    for entry in chunk:
        if 'latitudeE7' in entry and 'longitudeE7' in entry:
            lat = entry['latitudeE7'] / 1e7  # Convert latitudeE7 to decimal degrees
            lng = entry['longitudeE7'] / 1e7  # Convert longitudeE7 to decimal degrees
            timestamp = entry.get('timestamp', 'Unknown Timestamp')

            try:
                # Attempt to parse the timestamp with milliseconds
                formatted_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y")
            except ValueError:
                try:
                    # If parsing with milliseconds fails, try without milliseconds
                    formatted_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
                except ValueError:
                    # If both formats fail, set the formatted_date to the original timestamp
                    formatted_date = timestamp

            location = geolocator.reverse((lat, lng), exactly_one=True)

            if location:
                location_name = location.raw.get('display_name', 'Unknown Location')
                location_list.append([formatted_date, location_name])
            else:
                print(f"Skipping location. Nominatim couldn't find the location for coordinates: ({lat}, {lng})")
        else:
            print(f"Skipping entry due to missing latitudeE7 or longitudeE7: {entry}")

# Write the results to a CSV file (visited_locations.csv)
with open('visited_locations.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Date Visited', 'Location Name'])
    csv_writer.writerows(location_list)

print("Results have been written to 'visited_locations.csv'")
