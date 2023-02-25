# WheresPy? sPyWhere - dirspy verification utility
# some dirspy folders may cause client.py to crash. use this tool to check if they will.
import os
import configparser

def Test2(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        # print (path)
        if os.path.isdir(path):
            Test2(path)

config = configparser.ConfigParser()
config.read(r'wp.conf')
print("press ENTER to test folder: " + (config.get('client', 'dirspy')))
input("you will know the folder will not work if this utility crashes without showing an approval message.")
dirspy = (config.get('client', 'dirspy'))
Test2(dirspy)
f = open("dirspy.txt", "w+")
f.write("WheresPy? DirSpy for:" + "\n")
f.write(dirspy + "\n")
f.write("\n")
for lists in os.listdir(dirspy):
    f.write(os.path.join(dirspy, lists) + "\n")
f.close()
print("dirspy will work for this folder. make sure to remove the newly created 'dirspy.txt' file.")
input("press ENTER to exit.")