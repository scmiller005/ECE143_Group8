import os
import pandas as pd

# Define the folder containing AADT files
aadt_folder = r"C:\Users\prana\Documents\UCSD_Acad\WI25\ECE_143\143_Proj\data\AADT"

# List all AADT files
aadt_files = [f for f in os.listdir(aadt_folder) if f.endswith('.xlsx')]

# Keywords to filter sheets
years_and_keywords = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', 'AADT', 'aadt', 'Truck', 'TRUCK', 'truck', 'Peak', 'Hour', 'Hours', 'Ramp']
### For AADT ###
# Function to standardize column names and add year column
def process_file(file_path, file_name):
    # Extract year from filename 
    year = int(file_name.split('-')[0])
    
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Find the correct sheet based on keywords
    correct_sheet = None
    for sheet in excel_file.sheet_names:
        if any(keyword in sheet for keyword in years_and_keywords):
            correct_sheet = sheet
            break
    
    if correct_sheet:
        print(f"Processing sheet: {correct_sheet} in file: {file_name}")
        df = pd.read_excel(file_path, sheet_name=correct_sheet)
        
        # Standardize column names
        df = standardize_aadt_cols(df)
        
        # Add a 'YEAR' column
        df['YEAR'] = year
        
        return df
    else:
        print(f"No matching sheet found in file: {file_name}")
        return pd.DataFrame()  # Return an empty DataFrame if no matching sheet is found

# Function to standardize column names
def standardize_aadt_cols(df):
    df = df.rename(columns={
        'ROUTE': 'RTE',
        'ROUTE_SFX': 'RTE_SFX',
        'COUNTY': 'CNTY',
        'LOCATION DESCRIPTION': 'DESCRIPTION'  # Corrected typo in column name
    })
    return df

# Process and combine all AADT files
aadt_data_list = []

for file in aadt_files:
    print(f"\nProcessing file: {file}")
    
    # Debugging: Check year extraction
    year = int(file.split('-')[0])
    print(f"Extracted Year: {year}")
    
    file_path = os.path.join(aadt_folder, file)
    
    # Process the file
    df = process_file(file_path, file)
    
    # Debugging: Check DataFrame size after processing
    if not df.empty:
        print(f"After processing, Rows: {len(df)}, Columns: {len(df.columns)}")
        print(f"Unique Years in DataFrame: {df['YEAR'].unique()}")
        aadt_data_list.append(df)
    else:
        print(f"Skipping file: {file} (no matching sheet found)")

# Debugging: Check number of DataFrames in the list
print(f"\nNumber of DataFrames in list: {len(aadt_data_list)}")

# Combine all data into a single DataFrame
aadt_combined = pd.concat(aadt_data_list, ignore_index=True)

# Debugging: Check combined DataFrame
print(f"\nCombined DataFrame, Rows: {len(aadt_combined)}, Columns: {len(aadt_combined.columns)}")
print(f"Unique Years in Combined DataFrame: {aadt_combined['YEAR'].unique()}")

# Save the combined data to a new file
aadt_combined.to_csv('combined_aadt_2017_2022.csv', index=False)

###Truck AADT###

# Define the folder containing Truck AADT files
truck_aadt_folder = r"C:\Users\prana\Documents\UCSD_Acad\WI25\ECE_143\143_Proj\data\Truck_AADT"

# List all Truck AADT files
truck_aadt_files = [f for f in os.listdir(truck_aadt_folder) if f.endswith('.xlsx')]


# Function to standardize column names and add year column
def process_truck_file(file_path, file_name):
    # Extract year from filename (assuming format: YYYY_filename.xlsx)
    year = int(file_name.split('-')[0])
    
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Find the correct sheet based on keywords
    correct_sheet = None
    for sheet in excel_file.sheet_names:
        if any(keyword in sheet for keyword in years_and_keywords):
            correct_sheet = sheet
            break
    
    if correct_sheet:
        print(f"Processing sheet: {correct_sheet} in file: {file_name}")
        df = pd.read_excel(file_path, sheet_name=correct_sheet)
        
        # Standardize column names
        df = standardize_truck_cols(df)
        
        # Add a 'YEAR' column
        df['YEAR'] = year
        
        return df
    else:
        print(f"No matching sheet found in file: {file_name}")
        return pd.DataFrame()  # Return an empty DataFrame if no matching sheet is found

# Function to standardize column names
def standardize_truck_cols(df):
    # Rename columns in older format to match newer format
    df = df.rename(columns={
        'POST MILE': 'POSTMILE',
        'VEHICLE AADT TOTAL': 'VEHICLE_AADT_TOTAL',
        'TRUCK AADT TOTAL': 'TRUCK_AADT_TOTAL',
        'TRUCK %TOT VEH': 'TRK_PERCENT_TOT',
        '_2_AXLE': 'TRK_2_AXLE',
        'YEAR VER/EST': 'YEAR_VER'
    })
    
    # Drop unnecessary columns
    columns_to_drop = ['YEAR_VER', 'TRK_2_AXLE_PCT', 'TRK_3_AXLE_PCT', 'TRK_4_AXLE_PCT', 'TRK_5_AXLE_PCT', 'EST']
    for col in columns_to_drop:
        if col in df.columns:
            df = df.drop(columns=[col])
    
    return df

# Process and combine all Truck AADT files
truck_aadt_data_list = []

for file in truck_aadt_files:
    print(f"\nProcessing file: {file}")
    
    # Debugging: Check year extraction
    year = int(file.split('-')[0])
    print(f"Extracted Year: {year}")
    
    file_path = os.path.join(truck_aadt_folder, file)
    
    # Process the file
    df = process_truck_file(file_path, file)
    
    # Debugging: Check DataFrame size after processing
    if not df.empty:
        print(f"After processing, Rows: {len(df)}, Columns: {len(df.columns)}")
        print(f"Unique Years in DataFrame: {df['YEAR'].unique()}")
        truck_aadt_data_list.append(df)
    else:
        print(f"Skipping file: {file} (no matching sheet found)")

# Debugging: Check number of DataFrames in the list
print(f"\nNumber of DataFrames in list: {len(truck_aadt_data_list)}")

# Combine all data into a single DataFrame
truck_aadt_combined = pd.concat(truck_aadt_data_list, ignore_index=True)

# Debugging: Check combined DataFrame
print(f"\nCombined DataFrame, Rows: {len(truck_aadt_combined)}, Columns: {len(truck_aadt_combined.columns)}")
print(f"Unique Years in Combined DataFrame: {truck_aadt_combined['YEAR'].unique()}")

# Save the combined data to a new file
truck_aadt_combined.to_csv('combined_truck_aadt_2017_2022.csv', index=False)

###Peak hours###
# Define the folder containing Peak Hour Volume files
peak_hour_folder = r"C:\Users\prana\Documents\UCSD_Acad\WI25\ECE_143\143_Proj\data\peak_hr_vol"

# List all Peak Hour Volume files
peak_hour_files = [f for f in os.listdir(peak_hour_folder) if f.endswith('.xlsx')]


# Function to process Peak Hour Volume files
def process_peak_hour_file(file_path, file_name):
    # Extract year from filename (assuming format: YYYY_filename.xlsx)
    year = int(file_name.split('-')[0])
    
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Find the correct sheet based on keywords
    correct_sheet = None
    for sheet in excel_file.sheet_names:
        if any(keyword in sheet for keyword in years_and_keywords):
            correct_sheet = sheet
            break
    
    if correct_sheet:
        print(f"Processing sheet: {correct_sheet} in file: {file_name}")
        df = pd.read_excel(file_path, sheet_name=correct_sheet)
        
        # Drop the 'PRE' column if it exists
        if 'PRE' in df.columns:
            print(f"Dropping 'PRE' column in file: {file_name}")
            df = df.drop(columns=['PRE'])
        
        # Add a 'YEAR' column
        df['YEAR'] = year
        
        return df
    else:
        print(f"No matching sheet found in file: {file_name}")
        return pd.DataFrame()  # Return an empty DataFrame if no matching sheet is found

# Process and combine all Peak Hour Volume files
peak_hour_data_list = []

for file in peak_hour_files:
    print(f"\nProcessing file: {file}")
    
    # Debugging: Check year extraction
    year = int(file.split('-')[0])
    print(f"Extracted Year: {year}")
    
    file_path = os.path.join(peak_hour_folder, file)
    
    # Process the file
    df = process_peak_hour_file(file_path, file)
    
    # Debugging: Check DataFrame size after processing
    if not df.empty:
        print(f"After processing, Rows: {len(df)}, Columns: {len(df.columns)}")
        print(f"Unique Years in DataFrame: {df['YEAR'].unique()}")
        peak_hour_data_list.append(df)
    else:
        print(f"Skipping file: {file} (no matching sheet found)")

# Debugging: Check number of DataFrames in the list
print(f"\nNumber of DataFrames in list: {len(peak_hour_data_list)}")

# Combine all data into a single DataFrame
peak_hour_combined = pd.concat(peak_hour_data_list, ignore_index=True)

# Debugging: Check combined DataFrame
print(f"\nCombined DataFrame, Rows: {len(peak_hour_combined)}, Columns: {len(peak_hour_combined.columns)}")
print(f"Unique Years in Combined DataFrame: {peak_hour_combined['YEAR'].unique()}")

# Save the combined data to a new file
peak_hour_combined.to_csv('combined_peak_hour_2017_2022.csv', index=False)