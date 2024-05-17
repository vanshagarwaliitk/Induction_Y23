import socket
import threading
import os

IP_ADDR = socket.gethostbyname(socket.gethostname())
client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
PORT = 5050
client.connect((IP_ADDR,PORT))

def send_file(file_path, client_socket): 
    with open(file_path, "r") as file:
            chunk = file.read()
            print(chunk)
            print(type(chunk))
            client_socket.send(chunk.encode())

def STORE(filename,client):
    current = os.getcwd()
    client.send("STORE".encode())
    client.send(filename.encode('utf-8'))
    # print(filename)
    # print(type(filename))
    # print(type(filename.encode()))
    current = current + "/" + f"{filename}"
    send_file(current, client)
    
def retrieve_file(client_socket, file_name):

    client_socket.send("RETRIEVE".encode())
    client_socket.send(f"{file_name}".encode())
    with open(file_name,"w") as file:
            chunk = client_socket.recv(1024)
            file.write(chunk)
    print("File retrieved successfully.")


def LIST ():
    
    client.send("LIST".encode())
   

def QUIT():
    
    client.send("QUIT".encode())
   



def send_message ():
    while True:
         try:
              message = input()
              if message == "LIST" :
                 LIST()
              if message == "QUIT" :
                 QUIT()
              if message == "STORE" :
                 filename = input ("Enter the file name\n")
                 STORE(filename,client)
              if message == "RETRIEVE" :
                 filename = input("Enter the file name\n")
                 retrieve_file(filename,client)
              else:
                client.send(message.encode())
         except Exception as e :
            print("An error occurred" ,e)
            client.close()
            break
       
def recieve_message():
    while True:
         try:
            message = client.recv(1024).decode()
            print(f"{message}")
         except Exception as e :
            print("An error occurred",e)
            client.close()
            break

t1 = threading.Thread(target=recieve_message)
t2  = threading.Thread(target=send_message)
t2.start()
t1.start()
