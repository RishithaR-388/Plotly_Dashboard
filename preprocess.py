import numpy as np
import pandas as pd
import math

## Load the dataframe
df = pd.read_csv("data/actual/Temperature_change_Data.csv")


temp_change = df["tem_change"].tolist()
all_countries = df["Country Name"].tolist()


### Scaling the dataframe
def preprocess(values):
    scaled_temp = []

    for i in values:
        ## add with 100 to convert -ve values to positive and log the values
        val = i + 100
        val = math.log10(val)
        scaled_temp.append(val)
    
    return scaled_temp
    
df["temp_vals"] = preprocess(temp_change)

average_temps = df.groupby('Country Name')['temp_vals'].mean()

# filling null values with the average temperature of the respective country
def fill_null_with_average(row):
    country = row['Country Name']
    temp_value = row['temp_vals']
    if pd.isnull(temp_value):
        return average_temps[country]
    return temp_value

# Apply the fill_null_with_average function to fill null values
df['scaled_temp'] = df.apply(fill_null_with_average, axis=1)

# print(df)

# mapping country to country codes
def country_code_mapping(data):

    # Creating a new DataFrame with only "Country Name" and "Country Code" columns and dropping the duplicates
    country_code_mapping_df = data[['Country Name', 'Country Code']].drop_duplicates()

    # Convert the DataFrame to a dictionary with "Country Name" as the key and "Country Code" as the value
    country_code_mapping = country_code_mapping_df.set_index('Country Name')['Country Code'].to_dict()

    ## using the country_code_mapping to replace the empty values of Country Code column
    data['Country Code'] = data.apply(lambda row: country_code_mapping[row['Country Name']] if pd.isnull(row['Country Code']) else row['Country Code'], axis=1)

    return data

# filling the empty values of Country Code column
df = country_code_mapping(df)

# Dropping the un-necessary columns
columns_to_drop = ['tem_change', 'temp_vals']
df = df.drop(columns_to_drop, axis=1)


## Save the dataframe
df.to_csv('data/preprocess/Processed_Temperature_Change_Data.csv')