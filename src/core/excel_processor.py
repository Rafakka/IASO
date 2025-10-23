import pandas as pd
from typing import List, Tuple, Dict
from .models import Contact

class ExcelProcessor:
    def __init__(self):
        self.required_columns = ['paciente']
        self.phone_columns = ['tel.recado', 'tel.celular']
        
    def load_contacts_from_excel(self, file_path: str) -> Tuple[List[Contact], List[Dict]]:
        """
        
        Returns:
            Tuple of (valid_contacts, error_entries)
            - valid_contacts: List of Contact objects ready for processing
            - error_entries: List of dicts with error information for logging
        """
        try:
            df = pd.read_excel(file_path)
            
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            available_phone_columns = [col for col in self.phone_columns if col in df.columns]
            if not available_phone_columns:
                raise ValueError(f"No phone columns found. Need one of: {self.phone_columns}")
            
            valid_contacts = []
            error_entries = []
            
            for index, row in df.iterrows():
                try:
                    phone, phone_error = self._get_phone_number_with_fallback(row)
                    
                    if phone_error:
                        error_entries.append({
                            'row_index': index + 2,
                            'name': str(row['paciente']).strip() if 'paciente' in row else 'Unknown',
                            'phone_attempted': self._get_phone_attempt(row),
                            'error': phone_error
                        })
                        continue
                    
                    contact = Contact(
                        name=str(row['paciente']).strip(),
                        phone=phone,
                        message=str(row.get('message', 'Hello from automated system')).strip(),
                        message_type=str(row.get('message_type', 'SMS')).upper()
                    )
                    valid_contacts.append(contact)
                    
                except Exception as e:
                    error_entries.append({
                        'row_index': index + 2,
                        'name': str(row['paciente']).strip() if 'paciente' in row else 'Unknown',
                        'phone_attempted': self._get_phone_attempt(row),
                        'error': f"Unexpected error: {str(e)}"
                    })
                    continue
            
            return valid_contacts, error_entries
            
        except Exception as e:
            raise Exception(f"Excel processing failed: {str(e)}")
    
    def _get_phone_number_with_fallback(self, row) -> Tuple[str, str]:
        """
        Returns:
            Tuple of (phone_number, error_message)
            - If valid: (phone_number, None)
            - If invalid: (None, error_message)
        """
        for phone_column in self.phone_columns:
            if phone_column in row and pd.notna(row[phone_column]):
                phone_str = str(row[phone_column]).strip()
                
                if not phone_str or phone_str == 'nan':
                    continue
                
                validation_error = self.validate_phone_format(phone_str)
                if validation_error:
                    continue
                else:
                    return phone_str, None
        
        attempted_phones = self._get_phone_attempt(row)
        return None, f"No valid phone number found. Attempted: {attempted_phones}"
    
    def validate_phone_format(self, phone: str) -> str:
        import re
        
        cleaned = re.sub(r'\s+', ' ', phone.strip())
        
        pattern = r'^\d{2}\s-\s\d{4}\s-\s\d{4}$'
        if not re.match(pattern, cleaned):
            return f"Invalid format. Expected 'XX - XXXX - XXXX', got '{phone}'"
        
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) != 10:
            return f"Should have exactly 10 digits, got {len(digits_only)}"
        
        ddd = digits_only[:2]
        valid_ddds = ['11', '12', '13', '14', '15', '16', '17', '18', '19', 
                     '21', '22', '24', '27', '28', '31', '32', '33', '34', 
                     '35', '37', '38', '41', '42', '43', '44', '45', '46', 
                     '47', '48', '49', '51', '53', '54', '55', '61', '62', 
                     '63', '64', '65', '66', '67', '68', '69', '71', '73', 
                     '74', '75', '77', '79', '81', '82', '83', '84', '85', 
                     '86', '87', '88', '89', '91', '92', '93', '94', '95', 
                     '96', '97', '98', '99']
        
        if ddd not in valid_ddds:
            return f"Invalid DDD: {ddd}"
        
        return None
    
    def _get_phone_attempt(self, row) -> str:
        """Get string representation of phone attempts for error reporting"""
        attempts = []
        for col in self.phone_columns:
            if col in row and pd.notna(row[col]):
                phone_str = str(row[col]).strip()
                if phone_str and phone_str != 'nan':
                    attempts.append(f"{col}: '{phone_str}'")
        return ', '.join(attempts) if attempts else 'No phone data'
    
    def validate_contacts(self, contacts: List[Contact]) -> List[Contact]:
        """Final validation - should not have any phone errors at this point"""
        valid_contacts = []
        for contact in contacts:
            error = self.validate_phone_format(contact.phone)
            if error:
                print(f"Warning: Previously valid contact {contact.name} now has error: {error}")
            else:
                valid_contacts.append(contact)
        return valid_contacts