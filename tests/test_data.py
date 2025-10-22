
import pandas as pd

test_data = [
    {"name": "John Doe", "phone": "+1234567890", "message": "Hello John!"},
    {"name": "Jane Smith", "phone": "+0987654321", "message": "Hi Jane!"},
    {"name": "Bob Wilson", "phone": "+1112223333", "message": "Hey Bob!"}
]

df = pd.DataFrame(test_data)
df.to_excel("test_contacts.xlsx", index=False)
print("Test Excel file created: test_contacts.xlsx")