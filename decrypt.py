# WheresPy? sPyWhere - decryption utility
import os
from cryptography.fernet import Fernet
print("WheresPy? decryption utility")

if os.path.isfile('filekey.key'):
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
if not os.path.isfile('filekey.key'):
    print("could not find filekey.key. please enter decryption key:")
    key = input("> ")
fernet = Fernet(key)

def decryptloop():
    print("...")
    with open(decryptfile, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(decryptfile, 'wb') as dec_file:
        dec_file.write(decrypted)
    input(decryptfile + " has been decrypted. you can now open it.")

while 1==1:
    decryptfile = input("enter name of file to be encrypted (INCLUDE .zip) or drag it into this window: ")
    if not os.path.isfile(decryptfile):
        print("file does not exist. try again.")
        print()
    if os.path.isfile(decryptfile):
        decryptloop()