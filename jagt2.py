import csv
import pandas as pd
import os
import requests
from datetime import datetime, timedelta

# Function to read spillested (now omraader) from omraader.txt
def read_omraader(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []

# Function to create a list of dates within a range
def generate_dates(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    return date_list

# Function to get sunrise and sunset times from the API
def get_sun_times(date):
    url = f"https://api.sunrisesunset.io/json?lat=55.491686&lng=9.479599&date={date}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request fails
        data = response.json()

        if 'results' not in data or 'sunrise' not in data['results'] or 'sunset' not in data['results']:
            print(f"Warning: Unexpected API response for date {date}")
            return "09:00", "00:01", "23:59"  # Default fallback values
        
        sunrise = data['results']['sunrise']
        sunset = data['results']['sunset']

        # Convert times from 12-hour format (AM/PM) to 24-hour format
        sunrise_time = datetime.strptime(sunrise, "%I:%M:%S %p").strftime("%H:%M")
        sunset_time = datetime.strptime(sunset, "%I:%M:%S %p").strftime("%H:%M")

        # Calculate modetid (1 hour before sunrise)
        sunrise_dt = datetime.strptime(sunrise, "%I:%M:%S %p")
        modetid_time = (sunrise_dt - timedelta(hours=1)).strftime("%H:%M")

        return sunrise_time, modetid_time, sunset_time

    except requests.exceptions.RequestException as e:
        print(f"Error fetching sun times for {date}: {e}")
        return "09:00", "00:01", "23:59"  # Default fallback values

# Function to generate CSV file
def generate_csv(filename, start_date, end_date, omraader_list):
    dates = generate_dates(start_date, end_date)
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Dato", "Tid", "Hjemmehold", "Udehold", "Spillested", "Modested", "Modetid", "Sluttidspunk"])
        
        for date in dates:
            formatted_date = date.strftime('%Y-%m-%d')
            tid, modetid, sluttidspunk = get_sun_times(formatted_date)
            
            for spillested in omraader_list:
                hjemmehold = spillested
                udehold = ""
                modested = ""
                
                writer.writerow([
                    date.strftime('%d/%m/%Y'),
                    tid,  # Now set to sunrise time
                    hjemmehold,
                    udehold,
                    spillested,
                    modested,
                    modetid,  # 1 hour before sunrise
                    sluttidspunk  # Sunset time
                ])

# Function to convert CSV to Excel
def csv_to_excel(csv_path):
    try:
        with open(csv_path, 'r', newline='') as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            delimiter = dialect.delimiter

        df = pd.read_csv(csv_path, delimiter=delimiter)
        excel_path = os.path.splitext(csv_path)[0] + ".xlsx"
        df.to_excel(excel_path, index=False)
        print(f"Excel file created successfully at: {excel_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to run the script
def main():
    start_date_str = input("Enter the start date (DD-MM-YYYY): ")
    end_date_str = input("Enter the end date (DD-MM-YYYY): ")
    
    try:
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y').date()
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y').date()
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY.")
        return
    
    omraader_list = read_omraader("omraader.txt")
    
    if not omraader_list:
        return
    
    output_filename = "matches.csv"
    generate_csv(output_filename, start_date, end_date, omraader_list)
    print(f"CSV file '{output_filename}' has been generated.")
    csv_to_excel(output_filename)

if __name__ == "__main__":
    main()
