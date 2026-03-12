
import pandas as pd
import json
import os

def read_excel_details(file_path):
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        # Load the spreadsheet
        xl = pd.ExcelFile(file_path, engine='openpyxl')
        data = {}
        
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name)
            # Take a sample to understand the layout
            # Including more rows/cols to be sure we see labels and values
            data[sheet_name] = df.iloc[:50, :20].astype(str).values.tolist()
            
        return data
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    file_path = r"d:\Users\USUARIO 2023\Desktop\INTERFAZ\CL7.xlsx"
    details = read_excel_details(file_path)
    print(json.dumps(details))
