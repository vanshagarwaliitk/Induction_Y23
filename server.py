import socket 
import threading 
import os 

PORT = 5050

IP_ADDR = socket.gethostbyname(socket.gethostname())
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

server.bind((IP_ADDR , PORT))

server.listen()
customer =[]
clients = []

def send_file(client_socket, file_path):
    try:
        with open(file_path, "r") as file:
                chunk = file.read()
                client_socket.send(chunk.encode())
    except Exception as e:
        print("An error occurred:", e)

class Admin:
    def Addnewuser(username , password):
        dict1 = {'name':username , 'password':password ,'status':'Unban'}
        clients.append(dict1)
    def BanUser(username):
        for item in clients:
            if item.get('name') == username:
                item['status'] = "banned"
                break
    def UnBanUser(username):
        for item in clients:
            if item.get('name') == username:
                item['status'] ="unbanned"
    def DeleteUser(username):
        for item in clients:
            if item.get('name') == username :
                clients.remove(item)
                print("User has been deleted successfully")
                current = os.getcwd()
                path =  current + f"/{username}"
                os.rmdir(path)
                break

def check_status ( username):
    for item in clients:
        if item.get('name') == username:
            if item['status'] == "banned" :
                return 0
            else :
                return 1
def accept_client():
    while True:
        client, address = server.accept()
        print(f"\nConnection received from {address}")

        # ASk the client whether he is a new user or not
        client.send("Are you a new user? Type Y or N\n".encode())
        c = client.recv(1024).decode()

        if c == 'Y':
            handle_new_user(client)
        else:
            handle_existing_user(client)  

def handle_new_user(client):
    client.send("Enter Your username:\n".encode())
    username = client.recv(1024).decode()
    
    client.send("Enter a strong password:\n".encode())
    password = client.recv(1024).decode()

    # Add new user to the system
    if input("Do you want to add the above user? (Type ADDUSER to confirm):") == "ADDUSER":
        Admin.Addnewuser(username, password)
        client.send("Congrats!! You have been successfully added.\n".encode())
        os.makedirs(f"{username}")
        handle_existing_user(client)
    else:
        client.send("You are not allowed. Contact admin.\n".encode())


def handle_existing_user(client):
    client.send("Do you want to login? Type Y or N\n".encode())
    c = client.recv(1024).decode()

    if c == 'Y':
        client.send("Enter your username:\n".encode())
        username = client.recv(1024).decode()

        client.send("Enter your password:\n".encode())
        password = client.recv(1024).decode()

        if check_credentials(username, password):
            client.send("Congrats!! You have logged in successfully.\n".encode())
            handle_logged_in_user(client, username)
        else:
            client.send("Invalid credentials. Try again later.\n".encode())
    else:
        client.send("Goodbye.\n".encode())

def handle_logged_in_user(client,Username):

    while True :
        c = client.recv(1024).decode()
        if c == "STORE":
            print("store")
            check = check_status(Username)
            if check == 1:
                print("file")
                filename = client.recv(1024).decode() 
                print(f"{filename}")
                file_data = client.recv(2048).decode()
                print(file_data)
                print(type(file_data))
                current = os.getcwd()
                user_dir = os.path.join(current, Username)
                file_path = os.path.join(user_dir, filename)
                print("file")
                try:
                    # Open the file in binary mode for writing
                    with open(file_path, "w") as file:
                        file.write(file_data)
                        # Receive and write the file data in chunks
                        
                            
                    client.send("Your file has been stored successfully".encode())
                except Exception as e:
                    client.send(f"An error occurred: {e}".encode())
            else:
                client.send("You have been banned by the admin".encode())
        
        elif c == "RETRIEVE" :
            try:
                file_name = client.recv(1024).decode()
                current = os.getcwd()
                file_path = current + "/" + f"{Username}" + "/" +f"{file_name}"
                if not os.path.exists(file_path):
                        print("File not found:", file_name)
                        return
                send_file(client, file_path)
                print("File sent successfully.")
            except Exception as e:
                    print("An error occurred:", e)

        elif c == "LIST":
            check = check_status(Username)
            if check :
                current = os.getcwd()
                path = path = current + f"/{Username}"
                for root , dirs , files in os.walk(path):
                    for file in files:
                        client.send((os.path.join(root,file)).encode())
            else :
                client.send("You has been banned by the admin".encode())
        if c =="QUIT":
            Username = client.recv(1024).decode()
            client.close()
            print(f"{Username} has left")


def check_credentials(username, password):
    for item in clients:
        if item.get('name') == username and item.get('password') == password:
            return True
    return False


def system(client):
    d = input()
    if d == "DELETEUSER":
        username = input("Enter username")
        Admin.DeleteUser(Username)
    if d == "BANUSER":
        username = input("Enter username")
        Admin.BanUser(username)
    if d == "UNBAN":
        username = input("Enter username")
        Admin.UnBanUser(username)

if __name__ == "__main__":
    accept_client()
