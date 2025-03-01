import pandas as pd
import numpy as np
import matplotlib as plt

pranav_AADT_2017_2022 = pd.read_csv('C:/Users/zyplo/Documents/GitHub/ECE 143/ECE143_Group8/Data/pranav_cleaned_data/AADT/combined_aadt_2017_2022.csv')
print(pranav_AADT_2017_2022.head())
print(pranav_AADT_2017_2022.describe())
print(pranav_AADT_2017_2022.value_counts())