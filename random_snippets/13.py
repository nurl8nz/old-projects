import openpyxl
from cryptography.fernet import Fernet

def load_key(filename):
    with open(filename, 'rb') as key_file:
        return key_file.read()

def encryption(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

file_path = 'chegevara2.xlsx'

wb = openpyxl.load_workbook(file_path)
sheet = wb.active

key = load_key('secret.key')

for row in sheet.iter_rows(min_row=2, max_col=4, values_only=False):
    value3 = row[2].value  
    value4 = row[3].value  

    if value3 is not None and value4 is not None:
        encrypted_value3 = encryption(value3, key)
        encrypted_value4 = encryption(value4, key)

        row[2].value = encrypted_value3
        row[3].value = encrypted_value4

wb.save(file_path)
