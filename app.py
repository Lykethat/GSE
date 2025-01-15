from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import secrets

# Load the functions file
from tools.functions import *

# Initiate the Flask application 
app = Flask(__name__)

# Define the paths for the JSON files
data_folder = "data"
attractions = load_json(os.path.join(data_folder, "attractions_modified.json"))
nationalities = load_json(os.path.join(data_folder, "nationalities.json"))
categories = load_json(os.path.join(data_folder, "categories.json"))
trip = load_json(os.path.join(data_folder, "trips.json"))
# Path to the attractions.json file
ATTRACTIONS_FILE = "data/attractions_modified.json"

# Load attractions from JSON file
def load_attractions():
    if os.path.exists(ATTRACTIONS_FILE):
        with open(ATTRACTIONS_FILE, "r") as file:
            return json.load(file)
    return []

def get_hotels():
    attractions = load_attractions()
    hotels = [attraction for attraction in attractions if attraction.get("properties", {}).get("category") == "hotel"]
    # print("Hotels:", hotels)  # Debug statement
    return hotels


TRIPS_FILE = "data/trips.json"

# Load or initialize trips.json
def load_trips():
    if os.path.exists(TRIPS_FILE):
        with open(TRIPS_FILE, "r") as file:
            return json.load(file)
    else:
        # Initialize with empty data if file doesn't exist
        return []
def save_trip(trip_data):
    trips = load_trips()
    trips.append(trip_data)
    with open(TRIPS_FILE, "w") as file:
        json.dump(trips, file, indent=4)

# Route to display the trip creation form
@app.route("/create_new_trip", methods=["GET", "POST"])
def create_new_trip():
    if request.method == "POST":
        # Generate unique ID for the trip
        trip_id = secrets.token_hex(4)  # Generates an 8-character alphanumeric ID
        # Get form data
        trip_name = request.form.get("number_of_days")  # Use appropriate input name
        number_of_days = request.form.get("number_of_days")
        budget = request.form.get("budget")
        hotel = request.form.getlist("hotel")

        # Construct the trip data
        trip_data = {
            "details": {
                "trip_name": trip_name,
                "number_of_days": number_of_days,
                "budget": "2000",
                "hotel": hotel,
            },
            "destinations": {},
            "trip_id": trip_id,
        }

        # Save the trip data to the JSON file
        save_trip(trip_data)

        # Redirect to a success page or another route
        return redirect(url_for("destinations", trip_id=trip_id))
    # Get hotels for the dropdown
    hotels = get_hotels()
    # print("Hotels passed to template:", hotels)  # Debug statement
    return render_template("create_trip.html", categories=categories.get("categories", []),hotels=hotels)

# @app.route("/success/<trip_id>")
# def success(trip_id):
#     return f"Trip created successfully! Your trip ID is {trip_id}"


# Count the number of IDs in trips.json
def count_trip_ids(trip_data):
    if "trips" in trip_data:
        return len(trip_data["trips"])
    return 0

# Helper function to save a JSON file
def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def count_ids_in_trips():
    # Ensure the trips.json file exists
    if not os.path.exists(trip):
        print("The trips.json file does not exist.")
        return 0

    # Load the JSON data
    with open(trip, "r") as file:
        trips_data = json.load(file)

    # Count the number of IDs
    if "trips" in trips_data:
        return len(trips_data["trips"])
    else:
        print("No 'trips' key found in the JSON file.")
        return 0


# Home Route
@app.route('/')
def auth():
    return render_template('auth.html',nationalities=nationalities.get("nationalities", []))

# Select Screen Route
@app.route('/select_action')
def select_action():
    return render_template('select_action.html')
# AI trip Route
@app.route('/ai_trip_creator')
def ai_trip_creator():
    return render_template('ai_trip_creator.html',categories=categories.get("categories", []))

# # Destinations Route
@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    if request.method == 'POST':
        # Handle search or filter here
        return redirect(url_for('destinations'))
    return render_template('destinations.html', categories=categories.get("categories", []), attractions=attractions)

# Route to display a specific attraction by string ID
@app.route("/attraction/<string:attraction_id>")
def attraction_details(attraction_id):
    # Find the attraction by ID
    attraction = next((a for a in attractions if a["attraction_id"] == attraction_id), None)
    if attraction:
        return render_template("attraction_details.html", attraction=attraction)
    else:
        return "Attraction not found", 404

# Route to add an attraction ID to trips.json
@app.route("/add_to_trip/<string:attraction_id>")
def add_to_trip(attraction_id):
    if "trips" not in trip:
        trip["trips"] = []

    if attraction_id not in trip["trips"]:
        trip["trips"].append(attraction_id)
        save_json(os.path.join(data_folder, "trips.json"), trip)

    return redirect(url_for("view_cart"))

# Route to view attractions in trips.json
# @app.route("/view_cart")
# def view_cart():
#     selected_attractions = [a for a in attractions if a["attraction_id"] in trip.get("trips", [])]
#     return render_template("trip_cart.html", attractions=selected_attractions)

@app.route("/view_cart")
def view_cart():
    # Load the trips.json file
    if os.path.exists(TRIPS_FILE):
        with open(TRIPS_FILE, "r") as file:
            trips = json.load(file)
    else:
        return "No trips available", 404

    # Get the first record in trips.json
    if not trips:
        return "No trips available", 404

    first_trip = trips[0]  # Get the first trip
    destination_ids = first_trip.get("destinations", [])  # Get the destination IDs

    # Filter attractions based on the destination IDs
    selected_attractions = [a for a in attractions if a["attraction_id"] in destination_ids]

    return render_template("trip_cart.html", attractions=selected_attractions, trip_details=first_trip.get("details"))


# # Route to view attractions in trips.json
# @app.route("/view_trips")
# def view_trips():
#     selected_attractions = [a for a in attractions if a["attraction_id"] in trip.get("trips", [])]
#     return render_template("view_trip.html", attractions=selected_attractions)

@app.route("/view_trips")
def view_trips():
     # Load the trips.json file
    if os.path.exists(TRIPS_FILE):
        with open(TRIPS_FILE, "r") as file:
            trips = json.load(file)
    else:
        return "No trips available", 404

    # Ensure trips exist
    if not trips:
        return "No trips available", 404

    # Combine all destinations from all trips
    all_destinations = []
    for trip in trips:
        all_destinations.extend(trip.get("destinations", []))

    # Filter attractions based on all destinations
    selected_attractions = [a for a in attractions if a["attraction_id"] in all_destinations]

    # Pass trips and their associated attractions to the template
    return render_template("view_trip.html", trips=trips, attractions=selected_attractions)

# Select Screen Route
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Route to view attractions in trips.json
@app.route("/trip_list")
def trip_list():
    return render_template('trip_list.html')

# get_route
# @app.route("/get_route")
# def get_route():
#     return render_template('get_route.html')

@app.route("/get_route", methods=["GET"])
def get_route():
    # Load trips.json
    with open(TRIPS_FILE, "r") as file:
        trips = json.load(file)
    first_trip = trips[0]  # Get the first trip

    # Load attractions
    attractions = load_attractions()

    # Pass destinations and attractions to the template
    destinations = first_trip.get("destinations", [])
    return render_template("get_route.html",attractions=attractions,destinations=destinations)



if __name__ == '__main__':
    app.run(debug=True)