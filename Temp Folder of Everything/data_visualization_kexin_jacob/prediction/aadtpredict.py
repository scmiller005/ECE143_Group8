import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Read all CSV files
file_paths = ["i5_2019_coordinates.csv", "i5_2020_coordinates.csv", 
              "i5_2021_coordinates.csv", "i5_2022_coordinates.csv"]
dfs = [pd.read_csv(file) for file in file_paths]

# Standardize column names (remove possible spaces)
for df in dfs:
    df.columns = df.columns.str.strip()

# Add Year column
years = [2019, 2020, 2021, 2022]
for df, year in zip(dfs, years):
    df["Year"] = year

# Merge data from all years
merged_df = pd.concat(dfs, ignore_index=True)

# Generate unique location ID (based on DIST, CNTY, POSTMILE)
merged_df["Location_ID"] = merged_df["DIST"].astype(str) + "_" + merged_df["CNTY"].astype(str) + "_" + merged_df["POSTMILE"].astype(str)

# Count occurrences of each Location_ID and keep only those that appear in all four years
location_counts = merged_df["Location_ID"].value_counts()
common_locations = location_counts[location_counts == 4].index  # Select locations that appear in all four years
filtered_df = merged_df[merged_df["Location_ID"].isin(common_locations)]

# Handle missing values: Remove rows with NaN in specified columns
filtered_df = filtered_df.dropna(subset=["VEHICLE_AADT_TOTAL", "TRUCK_AADT_TOTAL", "Latitude", "Longitude"])

# Predict AADT and Truck AADT
predictions = []
for location in common_locations:
    loc_df = filtered_df[filtered_df["Location_ID"] == location].sort_values(by="Year")

    # Ensure there are no NaN values
    if loc_df[["VEHICLE_AADT_TOTAL", "TRUCK_AADT_TOTAL"]].isnull().sum().sum() > 0:
        continue  # Skip locations with missing data

    # Train the AADT prediction model
    X = loc_df["Year"].values.reshape(-1, 1)
    y_aadt = loc_df["VEHICLE_AADT_TOTAL"].values
    y_truck_aadt = loc_df["TRUCK_AADT_TOTAL"].values

    model_aadt = LinearRegression().fit(X, y_aadt)
    model_truck_aadt = LinearRegression().fit(X, y_truck_aadt)

    # Predict for 2023-2025
    future_years = np.array([2023, 2024, 2025]).reshape(-1, 1)
    pred_aadt = model_aadt.predict(future_years)
    pred_truck_aadt = model_truck_aadt.predict(future_years)

    '''
    # Force the AADT predictions to be non-negative
    pred_aadt = np.maximum(pred_aadt, 0)
    pred_truck_aadt = np.maximum(pred_truck_aadt, 0)
    '''

    # Store predictions for future years
    for year, aadt, truck_aadt in zip([2023, 2024, 2025], pred_aadt, pred_truck_aadt):
        predictions.append({
            "DIST": loc_df["DIST"].iloc[0],
            "CNTY": loc_df["CNTY"].iloc[0],
            "POSTMILE": loc_df["POSTMILE"].iloc[0],
            "Latitude": loc_df["Latitude"].iloc[0],  # Include latitude and longitude
            "Longitude": loc_df["Longitude"].iloc[0],
            "Year": year,
            "AADT": int(aadt),
            "Truck AADT": int(truck_aadt)
        })

# Convert predictions to DataFrame and save
predictions_df = pd.DataFrame(predictions)
predictions_df.to_csv("predicted_AADT_2023-2025.csv", index=False)

print("Prediction completed, results saved to predicted_AADT_2023-2025.csv")
