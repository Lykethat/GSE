import requests

# Define your API key
API_KEY = "ae9c2188-0f60-42ed-af56-05403567b4cc"

# Define the coordinates of the three places (latitude, longitude)
place1 = (-7.9784361112,112.6432617) 
place2 = (-7.9672043112,112.6339554)   
place3 = (-7.9669898112,112.6520544)  

def get_route(coord1, coord2):
    # Set the endpoint URL
    url = f"https://graphhopper.com/api/1/route?point={coord1[0]},{coord1[1]}&point={coord2[0]},{coord2[1]}&vehicle=car&key={API_KEY}"

    # Send request to GraphHopper
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        route_distance = data['paths'][0]['distance']  # in meters
        route_time = data['paths'][0]['time']  # in seconds
        return route_distance, route_time
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Calculate routes between the three places
route1_to_2 = get_route(place1, place2)
print(f"Route 1 to 2: Distance = {route1_to_2[0]} meters, Time = {route1_to_2[1]} seconds")

route2_to_3 = get_route(place2, place3)
print(f"Route 2 to 3: Distance = {route2_to_3[0]} meters, Time = {route2_to_3[1]} seconds")

route3_to_1 = get_route(place3, place1)
print(f"Route 3 to 1: Distance = {route3_to_1[0]} meters, Time = {route3_to_1[1]} seconds")
