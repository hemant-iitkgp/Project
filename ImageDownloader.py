import os
import pandas as pd
import requests

def create_folders(base_folder, subdistricts):
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)
    for subdistrict in subdistricts:
        folder_path = os.path.join(base_folder, subdistrict)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

def download_street_view_images(api_key, latitude, longitude, serial_number, subdistrict, output_folder):
    base_url = "https://maps.gomaps.pro/maps/api/streetview"
    #https://maps.gomaps.pro/maps/api/streetview?size=<string>&key=your api key from gomaps.pro
    headings = [0,90,180,270]  # Camera directions
    
    for heading in headings:
        params = {
            "size": "640x640",  # Image resolution
            "location": f"{latitude},{longitude}",
            "heading": heading,
            "key": api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            image_name = f"{latitude}_{longitude}_{serial_number}_{heading}.jpg"
            image_path = os.path.join(output_folder, image_name)
            with open(image_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download image for {latitude}, {longitude} at heading {heading}.")
        # exit()

def main():
    # Replace with your Google API Key
    API_KEY = "AlzaSy7KYWvrcxRvGee9xLh6bMlKtTaNgVxx_XM"

    # Read the Excel file
    excel_file = "locations.xlsx"
    df = pd.read_excel(excel_file)

    # Folder setup
    base_folder = "images"
    subdistricts = [
        "SubDistrict-Chhanve", "SubDistrict-City", "SubDistrict-Hallia", 
        "SubDistrict-Jamalpur", "SubDistrict-Kone", "SubDistrict-Lalganj", 
        "SubDistrict-Manjhwan", "SubDistrict-Marihan Patehara", "SubDistrict-Naraynpur", 
        "SubDistrict-Pahadi", "SubDistrict-Rajgarh", "SubDistrict-Sikhar"
    ]
    create_folders(base_folder, subdistricts)

    # Loop through the rows and download images
    for index, row in df.iterrows():
        serial_number = row["S.No"]
        if(serial_number<4):continue
        for subdistrict in subdistricts:
            latitude_col = f"{subdistrict}(Latitude)"
            longitude_col = f"{subdistrict}(Longitude)"

            if pd.notna(row[latitude_col]) and pd.notna(row[longitude_col]):
                latitude = row[latitude_col]
                longitude = row[longitude_col]
                output_folder = os.path.join(base_folder, subdistrict)

                download_street_view_images(
                    API_KEY, latitude, longitude, serial_number, subdistrict, output_folder
                )
        # exit()

if __name__ == "__main__":
    main()
