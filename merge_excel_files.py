import os
import pandas as pd

# === 1. Configuration ===
folder_path = 'excel_files'  # 🔁 Folder where your 10 Excel files are stored
output_file = 'merged_output.xlsx'

# === 2. List all Excel files in the folder ===
excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx') or file.endswith('.xls')]

# === 3. Initialize an empty list to collect dataframes ===
merged_data = []

# === 4. Read and append each Excel file ===
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)
    merged_data.append(df)
    print(f"Loaded: {file} ({df.shape[0]} rows)")

# === 5. Combine all dataframes into one ===
combined_df = pd.concat(merged_data, ignore_index=True)

# === 6. Save the merged dataframe to a new Excel file ===
combined_df.to_excel(output_file, index=False)
print(f"\n✅ Successfully merged {len(excel_files)} files into '{output_file}'")
