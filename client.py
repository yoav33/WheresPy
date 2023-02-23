# WheresPy? CLIENT MAIN
import os.path
import zipfile
import time
import socket
import configparser
import datetime
import urllib.request
import subprocess
from mss import mss
from cryptography.fernet import Fernet
import platform

print("----------------")
print("WheresPy? CLIENT")
print("----------------")

if not os.path.isfile('wp.conf'):
    print("wp.conf file does not exist! aborting.")
    exit()

config = configparser.ConfigParser()
config.read(r'wp.conf')
if ((config.get('general', 'runsetup'))=="y"):
    print("DS/G has not been configured yet!")
    print("you can configure through setup.py or by manually editing wp.conf.")
    input("press ENTER to exit.")
    exit()

print("device name: " + (config.get('client', 'devicename')))

# function: write out tree
def Test2(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        # print (path)
        if os.path.isdir(path):
            Test2(path)

# main loop (write files)
while ((config.get('client', 'dormant'))=="off"):
    print("----- creating new report -----")
    ti = time.time()
    now = datetime.datetime.now()
    date_string = now.strftime('%y-%m-%d %H-%M')
    os.mkdir(date_string)
    os.chdir(date_string)
    print("timestamp: " + date_string)

    # make info text file:
    f = open("general.txt", "w+")
    f.write("WheresPy? Device Report\n")
    f.write("Find on GitHub: https://github.com/yoav33/WheresPy\n")
    f.write("\n")
    f.write("Device name: " + config.get('client', 'devicename') + "\n")
    f.write(f"Platform info: {(platform.uname())} + \n")
    f.write("\n")
    f.write("Report timestamp: " + date_string + " (DD-MM-YY HH-MM)\n")
    f.write("\n")
    f.close()

    if ((config.get('client', 'dirspy'))=="N"):
        print("dirspy set to N. skipping...")
    else:
        dirspy = (config.get('client', 'dirspy'))
        print("creating dirSpy for " + dirspy)
        Test2(dirspy)
        f = open("dirspy.txt", "w+")
        f.write("WheresPy? DirSpy for:" + "\n")
        f.write(dirspy + "\n")
        f.write("\n")
        for lists in os.listdir(dirspy):
            f.write(os.path.join(dirspy, lists) + "\n")
        f.close()

    # make networking text file:
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print("public ip: " + external_ip)
    f = open("networking.txt", "w+")
    f.write(config.get('client', 'devicename') + " networking details\n")
    f.write("Public IP: " + external_ip + "\n")
    f.write("IPv4 address: " + socket.gethostbyname(socket.gethostname()) + "\n")
    devices = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    devices = devices.decode('ascii')
    devices = devices.replace("\r", "")
    f.write(devices)
    f.close()

    # screenshot
    with mss() as sct:
        sct.shot()

    # go back and make zip
    os.chdir('..')
    name = date_string
    zip_name = name + '.zip'
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for folder_name, subfolders, filenames in os.walk(name):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_ref.write(file_path, arcname=os.path.relpath(file_path, name))
    zip_ref.close()
    print("zip created! path: " + os.getcwd())
    for f in os.listdir(date_string):
        os.remove(os.path.join(date_string, f))
    os.rmdir(date_string)

    #encrypt now
    if os.path.isfile('filekey.key'):
        print("encrypting...")
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        with open(date_string + (".zip"), 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        with open(date_string + (".zip"), 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        print("encryption finished")
    if not os.path.isfile('filekey.key'):
        print("filekey.key not found! skipping encryption...")

    tf = time.time()
    totalt = tf-ti
    print(f"time taken to create file: {totalt} seconds")

    # send file


    intfreq = int(config.get('client', 'freq'))
    print(f"waiting {intfreq}s before creating new report.")
    print()
    time.sleep(intfreq)

# dormant mode
while ((config.get('client', 'dormany'))=="on"):

    # first connect to DORMANT server
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
    s.connect((config.get('server', 'serverip'), config.get('server', 'serverport')))
    msg = s.recv(1024)
    while msg:
        print('Received:' + msg.decode())
        msg = s.recv(1024)
        if msg=="screenshot":
            print("screenshot")