import zipfile
import json
import os

# --- CONFIGURATION ---
PBIT_PATH = r"C:\Users\PorselviSenthilkumar\Downloads\Power BI to DOMO\super store.pbit"

def extract_raw_pbi_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    raw_output = {
        "fileContent": None,
        "layoutInput": None
    }

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # 1. EXTRACT DATAMODELSCHEMA (Backend)
            if "DataModelSchema" in z.namelist():
                with z.open("DataModelSchema") as f:
                    raw_bytes = f.read()
                    try:
                        # Decode and immediately parse to a Python Object
                        # so we can 'Pretty Print' it later
                        raw_output["fileContent"] = json.loads(raw_bytes.decode("utf-16"))
                    except:
                        raw_output["fileContent"] = json.loads(raw_bytes.decode("utf-8"))
            
            # 2. EXTRACT REPORT/LAYOUT (Frontend)
            if "Report/Layout" in z.namelist():
                with z.open("Report/Layout") as f:
                    raw_bytes = f.read()
                    try:
                        raw_output["layoutInput"] = json.loads(raw_bytes.decode("utf-16"))
                    except:
                        raw_output["layoutInput"] = json.loads(raw_bytes.decode("utf-8"))

        return raw_output

    except zipfile.BadZipFile:
        print("Error: The file is not a valid zip/PBIT.")
        return None

if __name__ == "__main__":
    data = extract_raw_pbi_data(PBIT_PATH)
    
    if data:
        # THE FIX: 'indent=4' creates the multi-line, readable format
        # 'sort_keys=True' is optional but helps with organization
        print(json.dumps(data, indent=4, sort_keys=False))