import threading
import math
import socket
import os
from pathlib import Path
import shutil
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

IP_ADDR = socket.gethostbyname(socket.gethostname())
port = 1234
server.bind((IP_ADDR,port))
server.listen()

print("Server is Listening")

def find_user(username):
    cwd = os.getcwd()
    f = os.path.join(cwd,"user.txt")
    with open(f, "r") as file:
        for line in file:
           user, password = line.strip().split(":")
           print(user)
           print(password)
           if user == username:
            return 1
    return 0

def find_password(username,password):
     cwd = os.getcwd()
     f = os.path.join(cwd,"user.txt")
     
     with open(f, "r") as file:
        for line in file :
            user , passw = line.strip().split(":")
            if(user == username and passw == password):
                return 1
     return 0



def authenticate_client(client):
    client.send("Are you a new user ? YES or NO ".encode())
    ans = client.recv(1024).decode()
    if(ans == "YES"):
        client.send("Do register yourself first.".encode())
        username = client.recv(1024).decode()
        print(username)
        while find_user(username):
            client.send(f"Username {username} is already existing. Please try with other name.".encode())
            username = client.recv(1024).decode()
        client.send("Password".encode())
        password = client.recv(1024).decode()
        client.send("Confirm password".encode())
        re_password = client.recv(1024).decode()
        while password!=re_password:
             client.send("Password do not match. Please try again.".encode())
             password = client.recv(1024).decode()
             client.send("Confirm password".encode())
             re_password = client.recv(1024).decode()
        client.send(f"Congrats {username}, You have been successfully added to our server. Please run the following command to know this server works \n man ftp".encode())
        with open("/Users/shyampremi/Desktop/Desktop/web/server/user.txt","a") as file:
            file.write(f"{username}:{password}\n")
        
        cwd = os.getcwd()
        cwd = os.path.join(cwd,"Data")
        path = os.path.join(cwd,username)
        os.makedirs(path, exist_ok=True)

        return 1,username 

    elif(ans == "NO"):
         username = client.recv(1024).decode()
         while not find_user(username):
            client.send(f"Username {username} does not exist.".encode())
            username = client.recv(1024).decode()
         client.send("User is find".encode())
         password = client.recv(1024).decode()
         while not find_password(username,password):
            client.send(f"Password is not correct: ".encode())
            password = client.recv(1024).decode()
         client.send(f"Hey {username}, You are successfully logged in to the server. Please run the following command to know this server works \n man ftp".encode())
         return 1,username
    else :
        client.close()
        return 0, username
   
def man_ftp(client):
    cwd = os.getcwd()
    f = os.path.join(cwd,"help.txt")
    with open(f,"r") as file:
        for line in file:
            client.send(line.encode())
        client.send(b"EOF")

def mkdir(client,username,dire):
    cwd = os.getcwd()
    path = os.path.join(cwd,"Data",username,dire)
    os.makedirs(path, exist_ok=True)
    
def cd(client,cwd,dire):
    path = os.path.join(cwd,dire)
    if os.path.exists(path):
       client.send(dire.encode())
       return 1, path
    else:
        client.send(f"{dire}: No such directory exists.".encode())
    return 0, path

def cd_dot_dot(client,cwd,username):
    print(cwd)
    parent_path = Path(cwd).parent
    parent_name = parent_path.name
    if parent_name == "Data":
        client.send("home".encode())
    elif parent_name == username :
        client.send("home".encode())
        cwd = str(parent_path)
    else:
        client.send(parent_name.encode())
        cwd = str(parent_path)
    return cwd

def ls(username,client,cwd):
    print(cwd)
    if not os.path.isdir(cwd):
        client.send(b"Error: Invalid directory")
        return
    items = os.listdir(cwd)
    if not items:
        message = "No files found."
    else:
        message = "\n".join(items)
    client.send(message.encode())

def put(cwd,client,file_name):
    client.send(f"Finding the {file_name} in the current directory......".encode())
    message = client.recv(1024).decode()
    if message == "error":
        return
    file_path = os.path.join(cwd,file_name)
    
    file_size = int(message)
    print("Recieving file data")

    with open(file_path,'w') as file:
         recieved_size = 0
         while recieved_size < file_size:
            message = client.recv(1024).decode()
            if not message:
                break
            file.write(message)
            recieved_size+=len(message)

def get(cwd,file_name,client):
    file_path = os.path.join(cwd,file_name)
    if not os.path.exists(file_path):
        client.send("error".encode())
    else:
        file_size = os.path.getsize(file_path)
        client.send(f"{file_size}".encode())
        with open(file_path,"r") as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client.send(data.encode())

def delete(client,cwd,file_name):
    file_path = os.path.join(cwd,file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
        client.send("file removed successfully".encode())
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
        client.send("file removed successfully".encode())
    else:
        client.send("No such thing exists.".encode())

def mput(cwd,client,name):
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


def handle_client(client):
    status,username = authenticate_client(client)
    cwd = os.getcwd()
    parent_dir = os.path.join(cwd,"Data")
    cwd = os.path.join(cwd,"Data",username)
    if(status == True):
        while True:
            message = client.recv(1024).decode()
            if(message == "man ftp"):
                man_ftp(client)
            elif message.startswith("mkdir"):
                mkdir(client,username,message.strip().split(" ")[1])
            elif message == "cd..":
                 print(cwd)
                 cwd = cd_dot_dot(client,cwd,username)
                 path = Path(cwd)
                 parent_dir = path.parent
            elif message.startswith("cd"):
                print(message.strip().split(" ")[1])
                val,pre_cwd = cd(client,cwd,message.strip().split(" ")[1])
                print(val)
                print(pre_cwd)
                if val == 1:
                    parent_dir = cwd
                    cwd = pre_cwd
            elif message == "ls":
                ls(username,client,cwd)
            elif message.strip().split(" ")[0]=="put":
                file_name = message.strip().split(" ")[1]
                put(cwd,client,file_name)
            elif message.strip().split(" ")[0] == "get":
                file_name =  message.strip().split(" ")[1]
                get(cwd,file_name,client)
            elif message == "exit":
                client.close()
                break
            elif message.strip().split(" ")[0] == "delete":
                file_name = message.strip().split(" ")[1]
                delete(client,cwd,file_name)
            elif message.strip().split(" ")[0] == "mput":
                file_names = message.strip().split()[1:]
                print(file_names)
                for name in file_names:
                  mput(cwd,client,name)
            elif message.strip().split(" ")[0] == "mget":
                file_names = message.strip().split()[1:]
                flag = True
                for name in file_names:
                    file_path = os.path.join(cwd,name)
                    if not os.path.exists(file_path):
                        flag = False
                        client.send(f"{file_path} does not exist.".encode())
                        break
                    if os.path.isdir(file_path):
                        flag = False
                        client.send("You only can upload file onto the server.".encode())
                        break
                if flag :
                    for name in file_names:   
                        file_path = os.path.join(cwd,name)
                        file_size = os.path.getsize(file_path)
                        client.send(f"{file_size}".encode())
                        with open (file_path,"r") as file:
                            data = file.read(1024)
                            if not data:
                                break
                            client.send(data.encode())
             
def accept_client():
    while True:
        client,addr = server.accept()
        print(f"A client is connected to the server at {addr}")
        t = threading.Thread(target=handle_client,args=(client,))
        t.start()

if __name__ == "__main__":
    accept_client()
