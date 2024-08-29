import pandas as pd
import requests
from io import StringIO
import os
import json
import re  # Import regex module

# Function to clean column names by removing reference markers and redundant parts
def clean_column_names(column_name):
    # Convert column name to string
    column_name = str(column_name)
    # Remove reference markers like [44], [45]
    column_name = re.sub(r'\[\d+\]', '', column_name)
    # Remove redundant parts after cleaning
    column_name = ' '.join(dict.fromkeys(column_name.split()))
    return column_name.strip()

# Function to fetch and process the tables from the URL
def fetch_and_process_tables(url):
    # Set a proper User-Agent for the request
    headers = {"User-Agent": "MyApp/1.0 (https://example.com/myapp; myemail@example.com)"}

    # Fetch the HTML content from the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        return None

    # Read all tables from the HTML content using StringIO
    tables = pd.read_html(StringIO(response.text))

    # Check if any tables were found
    if not tables:
        print("No tables found on the page.")
        return None

    # Initialize a dictionary to store all tables
    all_tables = {}

    # Iterate over all tables and clean them
    for i, df in enumerate(tables):
        # Flatten multi-index columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [' '.join(col).strip() for col in df.columns.values]
        
        # Clean column names by converting them to strings and removing reference markers and redundant parts
        df.columns = [clean_column_names(str(col)) for col in df.columns]
        
        # Drop any rows that are fully NaN, if applicable
        df.dropna(how='all', inplace=True)
        
        # Convert the cleaned DataFrame to a JSON format
        json_data = df.to_dict(orient='records')
        
        # Store the cleaned table in the dictionary with a unique key
        all_tables[f'table_{i + 1}'] = json_data

    return all_tables

# Main function to interact with the user
def main():
    # Accept user input for the URL
    url = input("Enter the URL of the Wikipedia page: ").strip()

    # Simple validation to check if the URL is valid
    if not re.match(r'^https?://', url):
        print("Invalid URL format. Please provide a valid URL starting with http:// or https://.")
        return

    # Process the URL and fetch tables
    all_tables = fetch_and_process_tables(url)

    if all_tables:
        # Define the filename for the combined JSON file
        combined_json_filename = 'combined_tables.json'

        # Combine all tables into a single JSON file
        with open(combined_json_filename, 'w', encoding='utf-8') as combined_json_file:
            json.dump(all_tables, combined_json_file, indent=4, ensure_ascii=False)

        print(f"Combined JSON file '{combined_json_filename}' has been created successfully.")

if __name__ == "__main__":
    main()
