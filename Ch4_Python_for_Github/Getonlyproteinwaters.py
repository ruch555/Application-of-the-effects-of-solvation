import pandas as pd
import os
import io

def remove_rows_after_empty(filename):
    # Initialize an empty list to store valid lines
    valid_lines = []
    empty_row_found = False

    # Read the CSV file line by line
    with open(filename, 'r') as file:
        for line in file:
            # Check if the line is empty or contains only whitespace
            if not line.strip():
                empty_row_found = True
                break  # Stop reading lines after encountering the first empty row
            valid_lines.append(line)

    # Join the valid lines into a single string and read it as a DataFrame
    try:
        df = pd.read_csv(io.StringIO(''.join(valid_lines)))
    except pd.errors.ParserError as e:
        print(f"Error occurred while parsing CSV: {e}")
        return

    # Get the directory path and filename without extension
    directory = os.path.dirname(filename)
    filename_without_ext = os.path.splitext(os.path.basename(filename))[0]

    # Define the output directory
    output_directory = os.path.join(directory, "output")
    os.makedirs(output_directory, exist_ok=True)

    # Write the modified DataFrame to a new CSV file in the output directory
    new_filename = os.path.join(output_directory, f"{filename_without_ext}.csv")
    df.to_csv(new_filename, index=False)

    print("Modified file saved as:", new_filename)

def process_csv_files_in_folder(folder_path):
    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            remove_rows_after_empty(file_path)

# Call the function with the folder path containing CSV files
folder_path = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\csvfiles"
process_csv_files_in_folder(folder_path)
