import os
import sys

def test_your_scenario():
    print("🧪 TESTING YOUR FILE PATHS")
    
    test_files = [
        "test_contacts.xlsx",           # Same directory
        "../test_contacts.xlsx",        # Parent directory  
        "data/test_contacts.xlsx",      # Subdirectory
        "/absolute/path/to/contacts.xlsx"  # Absolute path
    ]
    
    for file_path in test_files:
        print(f"\nTesting: '{file_path}'")
        print(f"Exists: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            print(f"Absolute: {os.path.abspath(file_path)}")

if __name__ == "__main__":
    test_your_scenario()