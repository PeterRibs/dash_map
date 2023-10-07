import pandas as pd
import random
from geopy.distance import great_circle

import names

# Generate random data for 150 rural properties
property_data = {
    "Property Name": ["Property " + str(i) for i in range(1, 151)],
    "Latitude": [random.uniform(-33.75, 5.25) for _ in range(150)],  # Rough latitude range of Brazil
    "Longitude": [random.uniform(-73.98, -34.80) for _ in range(150)],  # Rough longitude range of Brazil
    "Area (hectares)": [random.uniform(10, 1000) for _ in range(150)],
    "Solar Energy": [random.choice(["Yes", "No"]) for _ in range(150)],
    "Number of Cows": [random.randint(0, 100) for _ in range(150)],
}

# Generate random data for property owners
owner_data = {
    "Owner Name": [names.get_full_name() for i in range(1, 151)],
}

print(owner_data)

# Create the DataFrame for property owners
owner_df = pd.DataFrame(owner_data)

# Generate random data for 50 veterinarians
veterinarian_data = {
    "Veterinarian Name": [names.get_full_name() for i in range(1, 51)],
    "Latitude": [random.uniform(-33.75, 5.25) for _ in range(50)],
    "Longitude": [random.uniform(-73.98, -34.80) for _ in range(50)],
}

# Create the DataFrame for veterinarians
vet_df = pd.DataFrame(veterinarian_data)

# Function to find the nearest veterinarian to a property
def find_nearest_vet(property_row):
    property_location = (property_row["Latitude"], property_row["Longitude"])
    vet_df["Distance"] = vet_df.apply(lambda row: great_circle(property_location, (row["Latitude"], row["Longitude"])).km, axis=1)
    nearest_vet = vet_df.loc[vet_df["Distance"].idxmin()]
    return nearest_vet["Veterinarian Name"]

# Add nearest veterinarian names to the property DataFrame
property_df = pd.DataFrame(property_data)
property_df["Owner Name"] = owner_df["Owner Name"]
property_df["Veterinarian"] = property_df.apply(find_nearest_vet, axis=1)

# Calculate milk collection
property_df["Milk Collection (liters/day)"] = property_df["Number of Cows"] * 20

# Save the dataframe 
property_df.to_csv("app/dataframe/property_df.csv", index=False)