import pandas as pd

test_data = [
    {
        "paciente": "João Silva", 
        "tel.recado": "11 - 9999 - 9999", 
        "tel.celular": "11 - 8888 - 8888",
        "message": "Olá João! Lembrete de consulta."
    },
    {
        "paciente": "", 
        "tel.recado": "11 - 9999 - 9999", 
        "tel.celular": "11 - 8888 - 8888",
        "message": "Olá Lembrete de consulta.",
        "data.solicitacao":"29/08/2025"
    },
    {
        "paciente": "Maria Santos", 
        "tel.recado": "",
        "tel.celular": "11 - 7777 - 7777",
        "message": "Olá Maria! Confirmação de horário.",
        "diagnostico":"cirurgia"
    },
    {
        "paciente": "Silva", 
        "tel.recado": "", 
        "tel.celular": "",
        "message": "Olá Silva! Lembrete de consulta."
    }
]

df = pd.DataFrame(test_data)
df.to_excel("test_contacts.xlsx", index=False)
print("✅ Created test_correct_contacts.xlsx with correct column names")