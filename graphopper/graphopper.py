from flask import Flask, render_template, jsonify
import json
import json
import requests
from itertools import combinations

app = Flask(__name__)


# GraphHopper API details
API_URL = "https://graphhopper.com/api/1/route"
API_KEY = "ae9c2188-0f60-42ed-af56-05403567b4cc"  # Replace with your GraphHopper API key

# Load JSON database
json_file_path = r"C:\Users\PC\Desktop\Ritsumeikan University\Year 3\Advanced Topics in Global Software Engineering\Intellitour\data\attractions_modified.json"  # Replace with your JSON file path

with open(json_file_path, "r") as file:
    places_data = json.load(file)

# Extract coordinates and names
locations = []
for place in places_data:
    # Validate keys
    name = place.get("name", "Unknown")
    coordinates = place.get("coordinates")
    if not coordinates or "lat" not in coordinates or "lon" not in coordinates:
        print(f"Skipping invalid entry: {place}")
        continue

    # Add valid location to the list
    locations.append({
        "id": place["id"],
        "name": name,
        "coordinates": f"{coordinates['lat']},{coordinates['lon']}"
    })

# Pair all locations for routing (can be adjusted to specific logic)
location_pairs = list(combinations(locations, 2))

# List to store route results
results = []

# Process each pair of locations
for pair in location_pairs:
    start = pair[0]
    end = pair[1]

    # Parameters for API request
    params = {
        "point": [start["coordinates"], end["coordinates"]],
        "vehicle": "car",
        "locale": "en",
        "key": API_KEY
    }

    # API call to GraphHopper
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        results.append({
            "start": {"id": start["id"], "name": start["name"]},
            "end": {"id": end["id"], "name": end["name"]},
            "route": data
        })
        print(f"Route from {start['name']} to {end['name']} retrieved successfully.")
    else:
        print(f"Failed to fetch route from {start['name']} to {end['name']}: {response.text}")


# Save the results to a new JSON file
output_file_path = "routes_results.json"
with open(output_file_path, "w") as file:
    json.dump(results, file, indent=4)

print(f"All routes processed. Results saved to {output_file_path}.")

@app.route('/')
def index():
    return render_template('index.html', routes=results)

if __name__ == '__main__':
    app.run(debug=True)









