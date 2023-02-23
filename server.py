# WheresPy? sPyWare - SERVER MAIN
import os

print("----------------")
print("WheresPy? SERVER")
print("----------------")
print("note: this server cannot control dormant machines.")
print("use 'dormantserver.py' for that.")
print()

# count files in server-in and print count
def count():
    count = 0
    for f in (os.listdir(indir)):
        count += 1
    print(f"files in {indir}: {count}")

# locate server-in folder. important!
# potential waste of lines? i don't care. i think the input is neat.
if not os.path.isdir('server-in'):
    dirin = input("'server-in' directory not found! enter 'continue' to create it, or enter the name of directory to be used: ")
    if dirin=="continue":
        os.mkdir("server-in")
        indir = 'server-in'
    else:
        indir = dirin
    exit()
else:
    indir = 'server-in'
    print("server-in found!")

# print(f"files in folder: {os.listdir(indir)})")
count()