import json
import random
import os
import string

def generate_random_id():
    """Generates a randomized 8-character alphanumeric value."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def get_unique_categories(data):
    """Extracts unique categories from the category field."""
    category_set = set()
    for feature in data:
        category = feature.get("properties", {}).get("category")
        if category:
            category_set.add(category)
    return ', '.join(sorted(category_set))

# Absolute or relative path to the data file
data_file_path = r"C:\Users\PC\Desktop\Ritsumeikan University\Year 3\Advanced Topics in Global Software Engineering\Intellitour\data\\"

# Construct the full file path
file_path = os.path.join(data_file_path, "attractions.json")

# Check if the file exists
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    # Process the data
    for feature in data:
        # Rename "type" to "attraction_id" and assign a random ID
        feature["attraction_id"] = generate_random_id().lower()
        feature.pop("type", None)  # Remove the original "type" field
        
        properties = feature.get("properties", {})
        
        # Make hospitals open 24/7 and assign random beds/rooms
        if properties.get("amenity") == "hospital":
            properties["opening_hours"] = "24/7"
            properties["beds"] = random.randint(0, 15)
            properties["rooms"] = random.randint(0, 15)
        
        # Combine "amenity", "shop", "tourism" into "category"
        category_fields = ["amenity", "shop", "tourism"]
        category_value = next((properties[field] for field in category_fields if properties.get(field) is not None), None)
        properties["category"] = category_value
        
        # Remove the original fields
        for field in category_fields:
            properties.pop(field, None)

    # Extract unique categories
    unique_categories = get_unique_categories(data)

    # Save the modified data
    output_file_path = os.path.join(data_file_path, "attractions_modified.json")
    with open(output_file_path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Modifications applied successfully. Updated data saved to '{output_file_path}'.")
    print(f"Unique categories: {unique_categories}")
else:
    print(f"Error: The file '{file_path}' does not exist.")
