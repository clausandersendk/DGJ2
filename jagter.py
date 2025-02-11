import csv
import pandas as pd
import os
import datetime

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
        current_date += datetime.timedelta(days=1)
    return date_list

# Function to generate random data for the CSV file
def generate_csv(filename, start_date, end_date, omraader_list):
    # Get the list of dates within the given range
    dates = generate_dates(start_date, end_date)
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Writing header
        writer.writerow(["Dato", "Tid", "Hjemmehold", "Udehold", "Spillested", "Modested", "Modetid", "Sluttidspunk"])
        
        for date in dates:
            for spillested in omraader_list:  # Each spillested gets a row for each date
                # Set "Tid" to always 09:00
                tid = "09:00"
                # set hjemmehold = Spillested
                hjemmehold = spillested
                # Leave , "Udehold", "Modested" empty
                udehold = ""
                modested = ""
                
                # Set "Modetid" to always 09:00 and "Sluttidspunk" to always 15:00
                modetid = "00:01"
                sluttidspunk = "23:59"
                
                # Write a row with the generated data
                writer.writerow([
                    date.strftime('%d/%m/%Y'),  # Format the date to 'DD/MM/YYYY'
                    tid,
                    hjemmehold,
                    udehold,
                    spillested,
                    modested,
                    modetid,
                    sluttidspunk
                ])

def csv_to_excel(csv_path):
    try:
        # Get the system's default delimiter
        with open(csv_path, 'r', newline='') as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            delimiter = dialect.delimiter

        # Load the CSV into a DataFrame with the detected delimiter
        df = pd.read_csv(csv_path, delimiter=delimiter)

        # Generate the Excel file path
        excel_path = os.path.splitext(csv_path)[0] + ".xlsx"

        # Save the DataFrame to Excel
        df.to_excel(excel_path, index=False)

        print(f"Excel file created successfully at: {excel_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to run the script
def main():
    # User inputs for date range
    start_date_str = input("Enter the start date (DD-MM-YYYY): ")
    end_date_str = input("Enter the end date (DD-MM-YYYY): ")
    
    # Parse the dates
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y').date()
        end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y').date()
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY.")
        return
    
    # Read the omraader list from omraader.txt
    omraader_list = read_omraader("omraader.txt")
    
    if not omraader_list:
        return  # Exit if omraader list is empty or the file was not found
    
    # Generate the CSV file
    output_filename = "matches.csv"
    generate_csv(output_filename, start_date, end_date, omraader_list)
    print(f"CSV file '{output_filename}' has been generated.")
    csv_to_excel(output_filename)    

if __name__ == "__main__":
    main()