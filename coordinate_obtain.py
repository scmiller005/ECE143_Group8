from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

def get_coordinates(input_file, output_file):
    # read csv file
    data = pd.read_csv(input_file)

    # initialize webdriver (make sure you have chromedriver)
    driver = webdriver.Chrome()

    # visit webpage
    url = "https://postmile.dot.ca.gov/"
    driver.get(url)
    time.sleep(2)  # waiting for the page to load

    # initialize result lists
    latitudes = []
    longitudes = []

    # loop through CSV data, auto-fill and query
    for index, row in data.iterrows():
        try:
            county = row["CNTY"]
            route = row["RTE"]
            postmile = row["POSTMILE"]

            # select County
            county_select = Select(driver.find_element(By.ID, "postmileCounty"))  
            county_select.select_by_value(county)

            # select Route
            route_select = Select(driver.find_element(By.ID, "postmileRoute"))
            route_select.select_by_value(str(route))

            # input Postmile
            postmile_input = driver.find_element(By.ID, "postmileValue")
            postmile_input.clear()
            postmile_input.send_keys(str(postmile))

            # click the query button
            go_button = driver.find_element(By.ID, "imPmGo")
            go_button.click()

            # wait for the query to complete
            time.sleep(3)

            # get latitude data
            lat_deg = driver.find_element(By.NAME, "LatDeg").get_attribute("value")
            lat_min = driver.find_element(By.NAME, "LatMin").get_attribute("value")
            lat_sec = driver.find_element(By.NAME, "LatSec").get_attribute("value")
            lat_dir = driver.find_element(By.NAME, "LatDir").get_attribute("value")  # N or S

            # convert to decimal format
            latitude = float(lat_deg) + float(lat_min) / 60 + float(lat_sec) / 3600
            if lat_dir == "S":
                latitude = -latitude

            # get longitude data
            lng_deg = driver.find_element(By.NAME, "LngDeg").get_attribute("value")
            lng_min = driver.find_element(By.NAME, "LngMin").get_attribute("value")
            lng_sec = driver.find_element(By.NAME, "LngSec").get_attribute("value")
            lng_dir = driver.find_element(By.NAME, "LngDir").get_attribute("value")  # E or W

            # convert to decimal format
            longitude = float(lng_deg) + float(lng_min) / 60 + float(lng_sec) / 3600
            if lng_dir == "W":
                longitude = -longitude

            print(latitude, longitude)
            latitudes.append(latitude)
            longitudes.append(longitude)

        except Exception as e:
            print(f"Error processing row {index}: {e}")
            latitudes.append("N/A")
            longitudes.append("N/A")

    # save results to output file
    data['Latitude'] = latitudes
    data['Longitude'] = longitudes
    data.to_csv(output_file, index=False)

    # close WebDriver
    driver.quit()
    print(f"Coordinates have been saved to {output_file}")

# call the function
get_coordinates("i5_2022.csv", "i5_2022_coordinates.csv")
