import pandas as pd
from typing import List
from .models import Contact

class ExcelProcessor:
    def __init__(self):
        self.required_columns = ['name', 'phone']
        
    def load_contacts_from_excel(self, file_path: str) -> List[Contact]:
        """Load and validate contacts from Excel file"""
        try:
            df = pd.read_excel(file_path)
            
            # Validate required columns
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Process each row
            contacts = []
            for _, row in df.iterrows():
                contact = Contact(
                    name=str(row['name']).strip(),
                    phone=self.clean_phone_number(str(row['phone'])),
                    message=str(row.get('message', 'Hello from automated system')).strip(),
                    message_type=str(row.get('message_type', 'SMS')).upper()
                )
                contacts.append(contact)
            
            return contacts
            
        except Exception as e:
            raise Exception(f"Excel processing failed: {str(e)}")
    
    def clean_phone_number(self, phone: str) -> str:
        """Clean and validate phone number"""
        # Remove non-digit characters except +
        cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
        
        # Basic validation
        if len(cleaned) < 10:
            raise ValueError(f"Invalid phone number: {phone}")
            
        return cleaned
    
    def validate_contacts(self, contacts: List[Contact]) -> List[Contact]:
        """Additional validation for contacts"""
        valid_contacts = []
        for contact in contacts:
            try:
                # Re-clean phone to ensure validity
                contact.phone = self.clean_phone_number(contact.phone)
                valid_contacts.append(contact)
            except ValueError as e:
                print(f"Skipping invalid contact {contact.name}: {e}")
        
        return valid_contacts