from flask import Flask, render_template, request, redirect, url_for
from tools.data import *
app = Flask(__name__)

@app.route('/')
def sign_in():
    return render_template('sign_in.html')

@app.route('/main', methods=['GET', 'POST'])
def main_search():
    if request.method == 'POST':
        # Handle search or filter here
        return redirect(url_for('main_search'))
    return render_template('main_search.html', labels=labels, attractions=attractions)

@app.route('/ai-trip', methods=['GET', 'POST'])
def ai_trip():
    if request.method == 'POST':
        # Handle AI trip selection here
        selection = request.form.get('trip_option')
        return f"You selected: {selection}"
    return render_template('ai_trip.html')

if __name__ == '__main__':
    app.run(debug=True)
