import pandas as pd
import json
import os
from datetime import datetime

def read_excel(file_path):
    df = pd.read_excel(file_path, sheet_name='Prüf-ID Prozessschritt')
    entries = []
    for _, row in df.iterrows():
        # Get anwendungsfall first as we might need it for aktion
        anwendungsfall = str(row.iloc[2]).strip().replace('--', '').replace('nan', '')
        aktion = str(row.iloc[9]).strip().replace('--', '').replace('nan', '')
        
        # If aktion is empty, use anwendungsfall
        if not aktion:
            aktion = anwendungsfall

        # Using column indices instead of names
        entry = {
            'ahb': str(row.iloc[1]),  # Column B (index 1)
            'anwendungsfall': anwendungsfall,  # Column C (index 2)
            'pruefidentifikator': str(row.iloc[3]),  # Column D (index 3)
            'prozessbeschreibung': str(row.iloc[5]),  # Column F (index 5)
            'aktion': aktion,  # Column E (index 4)
            'absender': str(row.iloc[10]),  # Column N (index 13)
            'empfaenger': str(row.iloc[11]),  # Column O (index 14)
            'zoobjekt': str(row.iloc[12]),  # Column P (index 15)
            'zovorfall': str(row.iloc[13]),  # Column Q (index 16)
            'zoerweitert': str(row.iloc[14]),  # Column R (index 17)
            'sparte': 'Gas' if str(row.iloc[17]).strip() == 'X' else ('Strom' if str(row.iloc[16]).strip() == 'X' else ''),  # Columns I and J
            'prozessschritt': str(row.iloc[8])  # Column G (index 6)
        }
        # Clean up the data
        for key, value in entry.items():
            if isinstance(value, str):
                entry[key] = value.strip().replace('--', '').replace('nan', '')
        entries.append(entry)
    return entries

def main():
    print("\nReading Excel file...")
    excel_file = os.path.join(os.path.dirname(__file__), 'PID_3_1_20241001.xlsx')
    entries = read_excel(excel_file)
    print(f"Found {len(entries)} entries in Excel")

    # Delete old processinfo.json if it exists
    old_json = os.path.join(os.path.dirname(__file__), 'processinfo.json')
    if os.path.exists(old_json):
        print(f"\nDeleting old JSON file: {old_json}")
        os.remove(old_json)

    # Create new JSON file (without timestamp, just processinfo.json)
    output_file = old_json
    
    print(f"\nCreating new JSON file: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    
    print(f"Created new JSON file with {len(entries)} entries")
    print("Done!")

if __name__ == "__main__":
    main()
