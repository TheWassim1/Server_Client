import socket
import threading
from cryptography.fernet import Fernet
import os
import pathlib
script_path = pathlib.Path(__file__).parent.resolve()
key_file_path = script_path / "TheKey.key"

if key_file_path.exists(): 
    with open("TheKey.key" , "rb") as key_file:
       key= key_file.read()
else:
    key=Fernet.generate_key()
    with open(key_file_path,"wb") as key_file:
        key_file.write(key)
cipher=Fernet(key)

HEADER = 64
PORT =5000
FORMAT ="utf-8"
#get the server ipv4 address automatically
SERVER = socket.gethostbyname(socket.gethostname())
ADDR =(SERVER,PORT)
DISCONNECTmsg ="disconnect"
#Create a TCP IPv4 socket so it can send and recieve data over a network
server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#attaching the socket to that IP and port
server.bind(ADDR)

def handle_client(conn , addr) :
    print(f"[NEW CONNECTION] {addr} connected.")
    connected =True
    try :
        host_name=socket.gethostbyaddr(addr[0])[0]
    except:
        host_name=addr[0]
    while connected :
        msg_length= conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length= int(msg_length)
            encrypted_msg=conn.recv(msg_length)
            try: 
                msg =cipher.decrypt(encrypted_msg).decode(FORMAT)
                print(f"[{host_name}] {msg}")  
                if msg ==DISCONNECTmsg:
                    connected=False
            except Exception as e :
                print(f"Eroor Decrypting: {e}")
                connected=False

            # elif msg in ["Hello" , "Hi" ,"Asselema"]:
            #     response=f"Hello {host_name} ,I am the Server!"
            #     conn.send(response.encode(FORMAT))
            # elif msg =="Goodbye":
            #     response="Type 'disconnect' to disconnect from the Server"
            #     conn.send(response.encode(FORMAT))
            # else :
            #     response="[Pro Tips] : Type 'help' for more commands"
            #     conn.send(response.encode(FORMAT))
    conn.close()
def start():
    #start listening for incoming connections
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True :
        #Creates a new socket (conn) for that client and gets the client address (addr)
        conn , addr =server.accept()
        thread =threading.Thread(target=handle_client , args=(conn ,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count()-1}")
print("Server is starting...")
start()
