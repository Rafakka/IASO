# debug_excel_reading.py
import pandas as pd
import os

def debug_excel_reading():
    # Let's see what pandas actually does
    file_path = "test_contacts.xlsx"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} does not exist!")
        return
    
    print(f"✅ File found: {file_path}")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    
    # Read the Excel file
    try:
        df = pd.read_excel(file_path)
        print("✅ Excel file read successfully!")
        
        # Show what pandas found
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print(f"Column names: {list(df.columns)}")
        
        # Show first few rows
        print("\n📊 First 3 rows of data:")
        print(df.head(3))
        
        # Show data types
        print("\n📝 Data types:")
        print(df.dtypes)
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

if __name__ == "__main__":
    debug_excel_reading()