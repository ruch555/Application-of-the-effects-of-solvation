#!DEFAULT ALL ATOMS TO C INSTEAD OF O!
import pandas as pd
import os

def find_common_waters(csv_folder, pdb_folder, output_folder):
    # Iterate over files in the CSV folder
    for csv_filename in os.listdir(csv_folder):
        if csv_filename.endswith(".csv"):
            # Extract base filename (without extension)
            csv_basename = os.path.splitext(csv_filename)[0]
            csv_file = os.path.join(csv_folder, csv_filename)

            # Read the CSV file
            data = pd.read_csv(csv_file)

            # Filter rows based on values in the "Fate" column
            filtered_data = data[data['Fate'].isin(['Absolute Displacement', 'Contact Displaced Bulk', 'Contact Displaced HF', 'Contact SWB',
                                                    'Contact SWH Lig HB', 'Contact SWH Prot HB'])]

            # Initialize a set to store values from column 1 of the Excel data
            prot_wat_values = set(filtered_data['Prot Water Number'])

            # Check if there is a corresponding PDB file
            pdb_filename = f"{csv_basename}.pdb"
            pdb_file = os.path.join(pdb_folder, pdb_filename)

            if os.path.exists(pdb_file):
                # Initialize a set to store values from column 2 of the filtered PDB file
                pdb_wat_values = set()

                # Open the PDB file
                with open(pdb_file, 'r') as f:
                    # Iterate over each line in the file
                    for line in f:
                        # Check if the line starts with 'ATOM'
                        if line.startswith('ATOM'):
                            # Split the line into columns
                            columns = line.split()
                            # Check if the 4th column contains "WAT" and the 5th column contains "X"
                            if columns[3] == 'WAT' and columns[4] == 'X':
                                pdb_wat_values.add(int(columns[1]))

                # Find common values between prot_wat_values and pdb_wat_values
                common_values = prot_wat_values.intersection(pdb_wat_values)

                # Specify the path for the new PDB file
                new_pdb_file = os.path.join(output_folder, f"{csv_basename}.pdb")

                # Open the new PDB file in write mode
                with open(new_pdb_file, 'w') as new_pdb:
                    # Open the PDB file
                    with open(pdb_file, 'r') as f:
                        # Iterate over each line in the file
                        for line in f:
                            # Check if the line starts with 'ATOM'
                            if line.startswith('ATOM'):
                                # Split the line into columns
                                columns = line.split()
                                # Check if the 4th column contains "WAT" and the 5th column contains "X"
                                if columns[3] == 'WAT' and columns[4] == 'X':
                                    # Check if the water number in column 2 is in the common values set
                                    if int(columns[1]) in common_values:
                                        # Extract the coordinates from columns 7, 8, and 9
                                        x_coord = float(columns[6])
                                        y_coord = float(columns[7])
                                        z_coord = float(columns[8])
                                        # Write the line to the new PDB file with updated coordinates and third column as "C"
                                        new_pdb.write(
                                            f"{line[:13]}C {line[15:30]}{x_coord:8.3f}{y_coord:8.3f}{z_coord:8.3f}{line[54:]}")


# Specify input and output folders
csv_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\csvfiles"
pdb_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\ogpdb"
output_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\pdbintwat"

# Call the function to find common waters and write them to output PDB files
find_common_waters(csv_folder, pdb_folder, output_folder)


