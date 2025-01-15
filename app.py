from flask import Flask, render_template, request, redirect, url_for

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
@app.route("/view_cart")
def view_trips():
    selected_attractions = [a for a in attractions if a["attraction_id"] in trip.get("trips", [])]
    return render_template("trip_cart.html", attractions=selected_attractions)

# Route to view attractions in trips.json
@app.route("/view_trips")
def view_trips():
    selected_attractions = [a for a in attractions if a["attraction_id"] in trip.get("trips", [])]
    return render_template("trip_cart.html", attractions=selected_attractions)


# @app.route('/ai-trip', methods=['GET', 'POST'])
# def ai_trip():
#     if request.method == 'POST':
#         # Handle AI trip selection here
#         selection = request.form.get('trip_option')
#         return f"You selected: {selection}"
#     return render_template('ai_trip.html')

if __name__ == '__main__':
    app.run(debug=True)