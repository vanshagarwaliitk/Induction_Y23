import socket
import threading
import os
import time


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP_ADDR = socket.gethostbyname(socket.gethostname())
port = 1234
client.connect((IP_ADDR,port))
message = client.recv(1024).decode()
print(message)
username = ""

def authentication():
    global username
    yn = input()
    client.send(yn.encode())
    if yn == "YES":
        print(client.recv(1024).decode())
        username = input("Enter your username: ")
        client.send(f"{username}".encode('utf-8'))
        message =client.recv(1024).decode()
        while message!="Password":
            print(message)
            username = input()
            client.send(username.encode())
            message = client.recv(1024).decode()
        print(message)
        password = input()
        client.send(password.encode())
        message = client.recv(1024).decode()
        print(message)
        re_password = input()
        client.send(re_password.encode())
        message = client.recv(1024).decode()
        while message.startswith("P"):
            print(message)
            password = input("Enter your password: ")
            client.send(password.encode())
            message = client.recv(1024).decode()
            print(message)
            re_password = input()
            client.send(re_password.encode())
            message = client.recv(1024).decode()
        # message = client.recv(1024).decode()
        print(message)
    elif yn == "NO":
        username = input("Enter your username: ")
        client.send(username.encode())
        message = client.recv(1024).decode()
        while message.startswith("Username"):
            print(message)
            username = input("Enter your username: ")
            client.send(username.encode())
            message = client.recv(1024).decode()
        password = input("Enter your password: ")
        client.send(password.encode())
        message = client.recv(1024).decode()
        while message.startswith("Password"):
            print(message)
            password = input("Enter password again: ")
            client.send(password.encode())
            message = client.recv(1024).decode()
        print(message)
    else :
        print("Command not found. Please try again.")
        client.close()


authentication()

def recieve_ftp(client):
    man_string = ""
    while True:
        data = client.recv(1024).decode()
        if "EOF" in data:
            data = data.replace("EOF","")
            man_string+=data
            break
        man_string+=data
    print(man_string)

def mget(cwd,client,name):
    file_path =  os.path.join(cwd,name)
    message = client.recv(1024).decode()
    file_size= int(message)
    with open(file_path,"w") as file:
        r_size = 0
        while r_size < file_size:
            message = client.recv(1024).decode()
            if not message:
                break
            r_size +=len(message)
            file.write(message)


directory = "home"
while True:
    cmd = input(f"{username}@shyams-Ftp-Server {directory} % ")
    client.send(cmd.encode())
    if cmd == "man ftp":
        recieve_ftp(client)
    elif cmd.startswith("mkdir"):
        continue
    elif cmd == "ls":
        message = client.recv(1024).decode()
        print(message)
    elif cmd == "cd..":
        message = client.recv(1024).decode()
        directory = message
    elif cmd.startswith("cd"):
        message = client.recv(1024).decode()
        if message == cmd.strip().split(" ")[1]:
           directory = message
        else:
            print(message)
    elif cmd.strip().split(" ")[0]=="put":
        message = client.recv(1024).decode()
        print(message)
        file_name = cmd.strip().split(" ")[1]
        c_d = os.getcwd()
        f_d = os.path.join(c_d,file_name)

        if not os.path.exists(f_d):
            print("No such file exists.")
            client.send("error".encode())
            
        else:
            print("No error")
            file_size = os.path.getsize(f_d)
            
            client.send(f"{file_size}".encode())
            with open(f_d,"r") as file:
                   while True:
                     chunk = file.read(1024)
                     if not chunk:
                        break;
                     client.send(chunk.encode())
            
            print("Waiting for the system for completion ....")
            time.sleep(3)
    elif cmd.strip().split(" ")[0] == "get":
        file_name = cmd.strip().split(" ")[1]
        message = client.recv(1024).decode()
        if message == "error":
            print("No such file is found on the server.")
        else:
            file_size = int(message)
            cwd = os.getcwd()
            file_path = os.path.join(cwd,file_name)
            with open(file_path,"w") as file:
                received_size = 0
                while received_size < file_size:
                    message = client.recv(1024).decode()
                    if not message:
                        break
                    file.write(message)
                    received_size+=len(message)
    elif cmd == "exit":
        client.close()
        break
    elif cmd.strip().split(" ")[0] == "delete":
        file_name = cmd.strip().split(" ")[1]
        message = client.recv(1024).decode()
        if message.strip().split(" ")[0] == "No":
            print(message)
    elif cmd.strip().split(" ")[0] == "mput":
         file_names = cmd.strip().split()[1:]
         cwd = os.getcwd()
         flag = True
         for name in file_names:
             file_path = os.path.join(cwd,name)
             if not os.path.exists(file_path):
                 flag = False
                 print(f"{file_path} does not exist.")
                 break
             if os.path.isdir(file_path):
                 flag = False
                 print("You only can upload file onto the server.")
                 break
         print("Files are found")
         if flag == True:
             for name in file_names:
                 file_path = os.path.join(cwd,name)
                 file_size = os.path.getsize(file_path)
                 client.send(f"{file_size}".encode())
                 with open (file_path,"r") as file:
                     data = file.read(1024)
                     if not data:
                         break
                     client.send(data.encode())  
    elif cmd.strip().split(" ")[0] == "mget":
        cwd = os.getcwd()
        file_names = message.strip().split()[1:]
        print(file_names)
        for name in file_names:
            mget(cwd,client,name)
    elif cmd.strip()=="":
        continue
    else:
        print("No such command exists.")
