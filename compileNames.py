import os
import sys
import csv

def insert_space_after_last_number(file_name):
    for i in range(len(file_name) - 1, -1, -1):
        if file_name[i].isdigit():
            return file_name[:i+1]
    return file_name

def list_files_to_csv(folder_path, output_csv):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print("Folder doesn't exist.")
        return
    
    # Get all file names in the folder
    files = os.listdir(folder_path)
    
    # Modify file names
    modified_files = [insert_space_after_last_number(file_name) for file_name in files]
    
    # Write modified file names to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name'])
        for modified_file_name in modified_files:
            writer.writerow([modified_file_name])
    
    print(f"All file names from {folder_path} have been modified and written to {output_csv}")

# Example usage: Assuming folder named 'data' is in the same directory as the script
folder_name = 'transitcsvs'
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name)
output_csv = 'names.csv'  # Name of the output CSV file
list_files_to_csv(folder_path, output_csv)