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

# Destinations Route
@app.route('/destinations', methods=['GET', 'POST'])
def main_search():
    if request.method == 'POST':
        # Handle search or filter here
        return redirect(url_for('destinations'))
    return render_template('destinations.html', categories=categories.get("categories", []), attractions=attractions)

@app.route('/ai-trip', methods=['GET', 'POST'])
def ai_trip():
    if request.method == 'POST':
        # Handle AI trip selection here
        selection = request.form.get('trip_option')
        return f"You selected: {selection}"
    return render_template('ai_trip.html')

if __name__ == '__main__':
    app.run(debug=True)