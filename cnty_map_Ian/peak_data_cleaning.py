import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'combined_peak_hour_2017_2022.csv'
df = pd.read_csv(file_path)

# Keep only the specified columns
columns_to_keep = ['DI', 'RTE', 'CO', 'PM', 'AM_WAY_PHV', 'AM_HOUR', 'PM_WAY_PHV', 'PM_HOUR']
df = df[columns_to_keep]

# Filter the DataFrame based on the specified conditions
df = df[(df['RTE'] == 5) & (df['CO'].isin(['ORA', 'SD', 'LA']))]

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)

# Save the cleaned DataFrame to a new CSV file
output_file_path = 'peak_hour.csv'
df.to_csv(output_file_path, index=False)

# Load the i5_2022_coordinates.csv file into a DataFrame
coordinates_file_path = 'i5_2022_coordinates.csv'
coordinates_df = pd.read_csv(coordinates_file_path)
coordinates_df.rename(columns={'CNTY': 'CO', 'POSTMILE': 'PM'}, inplace=True)

# Merge the DataFrames on 'CO' and 'PM' columns
df = pd.merge(df, coordinates_df, how='left', on=['CO', 'PM'])

# Rename the columns for clarity
df.rename(columns={'Longitude': 'LONGITUDE', 'Latitude': 'LATITUDE'}, inplace=True)

# Remove rows with missing LONGITUDE and LATITUDE values
df.dropna(subset=['LONGITUDE', 'LATITUDE'], inplace=True)

# Keep only the specified columns
columns_to_keep = ['DI', 'RTE_x', 'CO', 'PM', 'AM_WAY_PHV', 'AM_HOUR', 'PM_WAY_PHV', 'PM_HOUR', 'LONGITUDE', 'LATITUDE']
df = df[columns_to_keep]

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Create new rows for PM_HOUR and PM_KD_FACTOR
pm_hour_df = df[['DI', 'RTE_x', 'CO', 'PM', 'PM_HOUR', 'LONGITUDE', 'LATITUDE']].copy()
pm_hour_df.rename(columns={'PM_HOUR': 'HOUR'}, inplace=True)
pm_hour_df['PHV'] = df['PM_WAY_PHV']

am_hour_df = df[['DI', 'RTE_x', 'CO', 'PM', 'AM_HOUR', 'LONGITUDE', 'LATITUDE']].copy()
am_hour_df.rename(columns={'AM_HOUR': 'HOUR'}, inplace=True)
am_hour_df['PHV'] = df['AM_WAY_PHV']

# Combine the AM and PM DataFrames
df = pd.concat([am_hour_df, pm_hour_df], ignore_index=True)

# Reorder the columns
df = df[['DI', 'RTE_x', 'CO', 'PM', 'HOUR', 'PHV', 'LONGITUDE', 'LATITUDE']]

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)

# Save the merged DataFrame to a new CSV file
output_file_path = 'peak_hour_with_coordinates.csv'
df.to_csv(output_file_path, index=False)
