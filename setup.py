# WheresPy? sPyWhere - setup
import os.path
import configparser
from cryptography.fernet import Fernet
# import IPy
print("-----------------")
print("WheresPy? config setup")
print("-----------------")
print()

# read wp.conf
if not os.path.isfile('wp.conf'):
    print("wp.conf file does not exist! check host folder.")
    print("aborting.")
    exit()

# start initial setup
config = configparser.ConfigParser()
config.read(r'wp.conf')
if ((config.get('general', 'runsetup'))=="y"):
    input('press ENTER to begin client setup.')
    print("note: previously edited values will not be changed.")
    print()
    sudevicename = input('enter a name to be used for this device (client): ')
    suserverip = input('enter ip of server: ')
    suserverport = input('enter port of server: ')
    sufreq = input('how often should client send reports? (seconds): ')
    susendip = input('should client send ip address? (y/n): ')
    susendnetworks = input('should client send log of local internet networks? (y/n): ')
    suscreenshot = input('should client send screenshots? (y/n): ')
    input('press ENTER to write new values to wp.conf... ')
    # write into wp.conf
    with open('wp.conf', 'r') as conffile :
        confdata = conffile.read()
        confdata = confdata.replace('runsetup=y', 'runsetup=n')
        confdata = confdata.replace('devicename=X', 'devicename=' + sudevicename)
        confdata = confdata.replace('serverip=X', 'serverip=' + suserverip)
        confdata = confdata.replace('serverport=X', 'serverport=' + suserverport)
        confdata = confdata.replace('sendnetworks=X', 'sendnetworks=' + susendnetworks)
        confdata = confdata.replace('freq=X', 'freq=' + sufreq)
        confdata = confdata.replace('sendip=X', 'sendip=' + susendip)
        confdata = confdata.replace('screenshot=X', 'screenshot=' + suscreenshot)
        print("new values have been written.")
    with open('wp.conf', 'w') as conffile:
        conffile.write(confdata)
else:
    print("runsetup has been set to N. skipping setup questions.")

print()
print("press ENTER to generate a cryptography key.")
print("you may exit if you are going to use your own.")
input("make sure to create it yourself (filekey.key) and add to host folder for encryption to work!")
key = Fernet.generate_key()
# string the key in a file
with open('filekey.key', 'wb') as filekey:
    filekey.write(key)
print()
print("keyfile.key has been created and setup is finished.")
print("you may now exit and delete setup.py")
print("note: you may also delete filekey.key on the server files to keep them secure.")
print("if filekey.key is not found on client, encryption will be skipped.")
print("there are further settings you can explore in wp.conf, check them out.")
print("i assume no responsibility for the outcomes of what you may use this software for.")
print("glhf!")
print("     -yoav33 on GitHub")
exit()