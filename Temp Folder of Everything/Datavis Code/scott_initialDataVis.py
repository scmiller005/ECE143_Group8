import pandas as pd
import matplotlib as plt
import seaborn as sns

df = pd.read_csv('C:/Users/zyplo/Documents/GitHub/ECE 143/ECE143_Group8/Data/pranav_cleaned_data/AADT/combined_aadt_2017_2022.csv')
# print("Head: \n", df.head(), "\n")
# print("Describe: \n", df.describe(), "\n")
# print("Value Counts: \n", df.value_counts(), "\n")

# Adding total hour/monthy/AADT counts to dataframe (ex. TOTAL_PEAK_HOUR = BACK_PEAK_HOUR + AHEAD_PEAK_HOUR)
df.insert(8, 'TOTAL_PEAK_HOUR', df['BACK_PEAK_HOUR'] + df['AHEAD_PEAK_HOUR'])
df.insert(9, 'TOTAL_PEAK_MADT', df['BACK_PEAK_MADT'] + df['AHEAD_PEAK_MADT'])
df.insert(10, 'TOTAL_AADT', df['BACK_AADT'] + df['AHEAD_AADT'])

# Removing all rows with PEAK_HOUR, PEAK_MADT, AADT NaN values
df.dropna(subset=['BACK_PEAK_HOUR', 'BACK_PEAK_MADT', 'BACK_AADT', 'AHEAD_PEAK_HOUR', 'AHEAD_PEAK_MADT', 'AHEAD_AADT'])

# Creating a sub-dataframe with only San Diego County data
sd_df = df[df['CNTY'] == 'SD'] 

# Graph 1: County vs Hourly Ahead + Back
## SORT ME
plt.figure.Figure(figsize=(30, 10))
sns.barplot(x='CNTY', y='TOTAL_PEAK_HOUR', data=df, order=df.sort_values('TOTAL_PEAK_HOUR').CNTY, color='blue', label='Total Peak Hour ADT')
plt.pyplot.xlabel('County')
plt.pyplot.ylabel('Hourly Traffic')
plt.pyplot.title('County vs Hourly Ahead + Back')
plt.pyplot.legend()
plt.pyplot.xticks(rotation=90)
plt.pyplot.show()

# Graph 2: County vs Monthly Ahead + Back
## SORT ME
plt.figure.Figure(figsize=(30, 10))
sns.barplot(x='CNTY', y='TOTAL_PEAK_MADT', data=df, order=df.sort_values('TOTAL_PEAK_MADT').CNTY, color='blue', label='Total Peak Monthly ADT')
plt.pyplot.xlabel('County')
plt.pyplot.ylabel('Monthly Traffic')
plt.pyplot.title('County vs Monthly Ahead + Back')
plt.pyplot.legend()
plt.pyplot.xticks(rotation=90)
plt.pyplot.show()

# Graph 3: County vs AADT Ahead + Back
## SORT ME
plt.figure.Figure(figsize=(30, 10))
sns.barplot(x='CNTY', y='TOTAL_AADT', data=df, order=df.sort_values('TOTAL_AADT').CNTY, color='blue', label='Total AADT')
plt.pyplot.xlabel('County')
plt.pyplot.ylabel('AADT')
plt.pyplot.title('County vs AADT Ahead + Back')
plt.pyplot.legend()
plt.pyplot.xticks(rotation=90)
plt.pyplot.show()

# Graph 4: Year vs Ahead + Back AADT in San Diego
plt.figure.Figure(figsize=(30, 10))
sns.lineplot(x='YEAR', y='TOTAL_AADT', data=sd_df, marker='o', label='Total AADT')
plt.pyplot.xlabel('Year')
plt.pyplot.ylabel('AADT')
plt.pyplot.title('Year vs Ahead + Back AADT in San Diego')
plt.pyplot.legend()
plt.pyplot.grid(True)
plt.pyplot.show()

# Graph 5: Year vs Ahead AADT, Year vs Back AADT in San Diego
fig, ax = plt.pyplot.subplots(figsize=(12, 6))
sns.lineplot(x='YEAR', y='AHEAD_AADT', data=sd_df, marker='o', label='Ahead AADT', color='red')
sns.lineplot(x='YEAR', y='BACK_AADT', data=sd_df, marker='s', label='Back AADT', color='blue')
plt.pyplot.xlabel('Year')
plt.pyplot.ylabel('AADT')
plt.pyplot.title('Year vs Ahead AADT, Year vs Back AADT in San Diego')
plt.pyplot.legend()
plt.pyplot.grid(True)
plt.pyplot.show()

# ADD MORE GRAPHS BY HIGHWAYS

# Comparison between normal traffic volume and truck volume by the 6 highways --> combined_truck_aadt >> truck percentage column

# Questions
# - For each of our 6 highways, what is the density of trucks vs cars?
# - Focusing on the highway with the most truck density, where are they the most dense?
# - How did COVID affect traffic? Car vs. truck
# - Where does the infrastructure need to be increased (prediction data w/ peak hour data to identify specific conjestion hotspots)