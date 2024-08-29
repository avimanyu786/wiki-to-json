import pandas as pd
import requests
from io import StringIO
import json
import re
import tkinter as tk
from tkinter import messagebox, filedialog

# Function to clean column names by removing reference markers and redundant parts
def clean_column_names(column_name):
    column_name = str(column_name)
    column_name = re.sub(r'\[\d+\]', '', column_name)  # Remove reference markers
    column_name = ' '.join(dict.fromkeys(column_name.split()))  # Remove redundant parts
    return column_name.strip()

# Function to fetch and process the tables from the URL
def fetch_and_process_tables(url):
    headers = {"User-Agent": "MyApp/1.0 (https://example.com/myapp; myemail@example.com)"}
    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            messagebox.showerror("Error", f"Error fetching page: {response.status_code}")
            return None

        tables = pd.read_html(StringIO(response.text))
        if not tables:
            messagebox.showerror("Error", "No tables found on the page.")
            return None

        all_tables = {}
        for i, df in enumerate(tables):
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [' '.join(col).strip() for col in df.columns.values]
            
            df.columns = [clean_column_names(str(col)) for col in df.columns]
            df.dropna(how='all', inplace=True)
            json_data = df.to_dict(orient='records')
            all_tables[f'table_{i + 1}'] = json_data

        return all_tables

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None

# Function to handle the button click event
def on_fetch_button_click():
    url = url_entry.get().strip()
    if not re.match(r'^https?://', url):
        messagebox.showerror("Invalid URL", "Please enter a valid URL starting with http:// or https://.")
        return

    all_tables = fetch_and_process_tables(url)
    if all_tables:
        save_file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_file_path:
            with open(save_file_path, 'w', encoding='utf-8') as combined_json_file:
                json.dump(all_tables, combined_json_file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Success", f"Combined JSON file has been created successfully at:\n{save_file_path}")

# Function to center the window on the screen
def center_window(window, width=400, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Main GUI setup
root = tk.Tk()
root.title("Wikipedia Tables to JSON Converter")
center_window(root, 500, 250)  # Center the window with desired dimensions
root.configure(bg='#f0f0f0')  # Set background color

# Styling
font_style = ("Helvetica", 12)
button_style = {"font": ("Helvetica", 12, "bold"), "bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5}

# URL entry field
tk.Label(root, text="Enter the URL of the Wikipedia page:", font=font_style, bg='#f0f0f0').pack(pady=10)
url_entry = tk.Entry(root, width=50, font=font_style)
url_entry.pack(pady=10)

# Fetch button
fetch_button = tk.Button(root, text="Fetch Tables and Save as JSON", command=on_fetch_button_click, **button_style)
fetch_button.pack(pady=20)

# Run the GUI main loop
root.mainloop()
