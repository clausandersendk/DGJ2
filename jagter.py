import csv
import pandas as pd
import os
import requests
from datetime import datetime, timedelta

# Read omraader from CSV
def read_omraader_csv(file_path):
    omraader = []
    try:
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row.get("Location") or not row.get("Latitude") or not row.get("Longitude"):
                    print(f"⚠️ Skipping incomplete or invalid row: {row}")
                    continue
                try:
                    omraader.append({
                        "location": row["Location"].strip(),
                        "lat": float(row["Latitude"]),
                        "lng": float(row["Longitude"])
                    })
                except ValueError:
                    print(f"⚠️ Skipping row with invalid lat/lng: {row}")
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found.")
    return omraader

# Generate a list of dates
def generate_dates(start_date, end_date):
    return [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# Get sun times (no need for timezone conversion since API already returns local time)
def get_sun_times(date, lat, lng):
    url = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&date={date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', {})
        sunrise = results.get('sunrise')
        sunset = results.get('sunset')

        if not sunrise or not sunset:
            raise ValueError("Missing sunrise/sunset in API response")

        # Directly use the API return values (no conversion necessary)
        sunrise_time = datetime.strptime(f"{date} {sunrise}", "%Y-%m-%d %I:%M:%S %p")
        sunset_time = datetime.strptime(f"{date} {sunset}", "%Y-%m-%d %I:%M:%S %p")

        # Modetid is 1 hour before sunrise
        modetid_time = (sunrise_time - timedelta(hours=1)).strftime("%H:%M")

        # Format times as hours and minutes
        sunrise_time = sunrise_time.strftime("%H:%M")
        sunset_time = sunset_time.strftime("%H:%M")

        return sunrise_time, modetid_time, sunset_time

    except Exception as e:
        print(f"❌ Error fetching sun times for {date} (lat: {lat}, lng: {lng}): {e}")
        return "09:00", "00:01", "23:59"

# Generate CSV file
def generate_csv(filename, start_date, end_date, omraader_list):
    dates = generate_dates(start_date, end_date)

    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Dato", "Tid", "Hjemmehold", "Udehold", "Spillested", "Modested", "Modetid", "Sluttidspunk"])

        for date in dates:
            formatted_date = date.strftime('%Y-%m-%d')
            for omraade in omraader_list:
                tid, modetid, sluttidspunk = get_sun_times(formatted_date, omraade["lat"], omraade["lng"])
                writer.writerow([
                    date.strftime('%d/%m/%Y'),
                    tid,
                    omraade["location"],
                    "",
                    omraade["location"],
                    "",
                    modetid,
                    sluttidspunk
                ])

# Convert CSV to Excel
def csv_to_excel(csv_path):
    try:
        df = pd.read_csv(csv_path)
        excel_path = os.path.splitext(csv_path)[0] + ".xlsx"
        df.to_excel(excel_path, index=False)
        print(f"✅ Excel file created successfully at: {excel_path}")
    except Exception as e:
        print(f"❌ An error occurred while converting to Excel: {e}")

# Main program
def main():
    start_date_str = input("Enter the start date (DD-MM-YYYY): ")
    end_date_str = input("Enter the end date (DD-MM-YYYY): ")

    try:
        start_date = datetime.strptime(start_date_str, '%d-%m-%Y').date()
        end_date = datetime.strptime(end_date_str, '%d-%m-%Y').date()
    except ValueError:
        print("❌ Invalid date format. Please use DD-MM-YYYY.")
        return

    omraader = read_omraader_csv("omraader.csv")
    if not omraader:
        print("❌ No valid omraader found.")
        return

    output_filename = "matches.csv"
    generate_csv(output_filename, start_date, end_date, omraader)
    print(f"✅ CSV file '{output_filename}' has been generated.")
    csv_to_excel(output_filename)

if __name__ == "__main__":
    main()
