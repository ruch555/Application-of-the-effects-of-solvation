# !WORKS ON FOLDERS FOR CLOSEST LIG ATOM - Make ligand based water constellation!
# import os
# import csv
#
# # Input folder paths for CSV and PDB files
# csv_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\csvfiles"
# pdb_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\pdbintwat"
# # Output folder path
# output_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\classifiedpdb"
#
# # Step 1: Process each CSV file
# for csv_file in os.listdir(csv_folder):
#     if csv_file.endswith('.csv'):
#         csv_path = os.path.join(csv_folder, csv_file)
#         pdb_file = os.path.splitext(csv_file)[0] + '.pdb'
#         pdb_path = os.path.join(pdb_folder, pdb_file)
#
#         # Step 1: Open and filter CSV file
#         filtered_data = []
#         with open(csv_path, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 if row['Fate'] in ['Absolute Displacement', 'Contact Displaced Bulk', 'Contact Displaced HF',
#                                    'Contact SWB', 'Contact SWH Lig HB', 'Contact SWH Prot HB']:
#                     filtered_data.append(row)
#
#         # Step 2: Record water numbers
#         water_numbers = [int(row['Prot Water Number']) for row in filtered_data]
#
#         # Step 3: Open and read PDB file
#         with open(pdb_path, 'r') as pdbfile:
#             lines = pdbfile.readlines()
#
#         # Step 4: Process PDB file
#         output_lines = []
#         for line in lines:
#             if line.startswith('ATOM'):
#                 atom_number = int(line[6:11].strip())
#                 if atom_number in water_numbers:
#                     index = water_numbers.index(atom_number)
#                     closest_lig_atom = filtered_data[index]['Closest Lig Atom'].strip()
#                     if closest_lig_atom and closest_lig_atom[0] in ['O']:
#                         line = line[:13] + "O" + line[14:]
#                     elif closest_lig_atom and closest_lig_atom[0] in ['N']:
#                         line = line[:13] + "N" + line[14:]
#                     else:
#                         line = line[:13] + "C" + line[14:]
#             output_lines.append(line)
#
#         # Step 5: Write output PDB file
#         output_pdb_path = os.path.join(output_folder, os.path.splitext(csv_file)[0] + '.pdb')
#         with open(output_pdb_path, 'w') as output_pdb:
#             output_pdb.writelines(output_lines)
#





# !WORKS ON FOLDERS FOR PROTHB - Make protein-interaction based water constellation!
import os
import csv

# Function to determine atom name based on category and column values
def determine_atom_name(category, protHB, protHF, distance):
    if category in ['Contact SWB', 'Contact SWH Prot HB']:
        return 'O'
    elif category in ['Contact Displaced HF', 'Contact SWH Lig HB']:
        return 'C'
    elif category == "Absolute Displacement":
        if protHB.lower() == 'true':
            return 'O'
        elif protHF.lower() == 'true':
            return 'C'
        else:
            return 'C' if float(distance) < 5 else 'O'
    elif category == "Contact Displaced Bulk":
        if protHB.lower() == 'true':
            return 'O'
        elif protHF.lower() == 'true':
            return 'C'
        else:
            return 'O'

# Function to process CSV and PDB files
def process_files(csv_folder, pdb_folder, output_folder):
    for csv_filename in os.listdir(csv_folder):
        if not csv_filename.endswith('.csv'):
            continue
        csv_path = os.path.join(csv_folder, csv_filename)
        pdb_filename = os.path.splitext(csv_filename)[0] + '.pdb'
        pdb_path = os.path.join(pdb_folder, pdb_filename)
        if not os.path.exists(pdb_path):
            print(f"Matching PDB file not found for '{csv_filename}'")
            continue

        # Open and read CSV file
        filtered_data = []
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Fate'] in ['Absolute Displacement', 'Contact Displaced Bulk', 'Contact Displaced HF',
                                   'Contact SWB', 'Contact SWH Lig HB', 'Contact SWH Prot HB']:
                    filtered_data.append(row)

        # Record water numbers and corresponding category, protHB, protHF, and distance
        water_info = {}  # Dictionary to store water numbers and their attributes
        for row in filtered_data:
            water_info[int(row['Prot Water Number'])] = {
                'category': row['Fate'],
                'protHB': row['ProtHB'],
                'protHF': row['ProtHF'],
                'distance': row['Distance']
            }

        # Open and read PDB file
        with open(pdb_path, 'r') as pdbfile:
            lines = pdbfile.readlines()

        # Process PDB file
        output_lines = []
        for line in lines:
            if line.startswith('ATOM'):
                atom_number = int(line[6:11].strip())
                if atom_number in water_info:
                    attributes = water_info[atom_number]
                    category = attributes['category']
                    protHB = attributes['protHB']
                    protHF = attributes['protHF']
                    distance = attributes['distance']
                    atom_name = determine_atom_name(category, protHB, protHF, distance)
                    line = line[:13] + atom_name + line[14:]
            output_lines.append(line)

        # Write output PDB file
        output_pdb_filename = os.path.splitext(csv_filename)[0] + '.pdb'
        output_pdb_path = os.path.join(output_folder, output_pdb_filename)
        with open(output_pdb_path, 'w') as output_pdb:
            output_pdb.writelines(output_lines)

# Specify input and output folders
csv_input_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\csvfiles"
                    # Replace with your CSV input folder path
pdb_input_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\pdbintwat"
                    # Replace with your PDB input folder path
output_folder = r"C:\Users\Ruchira J\Desktop\SOP\thesis\3DSim\python\classifiedpdb"
                    # Replace with your output folder path

# Process CSV and PDB files
process_files(csv_input_folder, pdb_input_folder, output_folder)
