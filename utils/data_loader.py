
# Import required library
import json  # For loading JSON data from file

# Function to load patient data from a JSON file
# Reads the file, parses the JSON, and returns the data as a Python object
def load_patient_data(file_path="data/patients.json"):
    with open(file_path, "r") as f:
        data = json.load(f)  # Load and parse JSON data
    return data  # Return patient data as list of dicts
