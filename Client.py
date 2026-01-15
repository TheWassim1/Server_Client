import socket
from cryptography.fernet import Fernet
key=open("TheKey.key" , "rb").read()
cipher=Fernet(key)

HEADER = 64
PORT = 5000
FORMAT = "utf-8"
DISCONNECTmsg = "disconnect"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def send(encrypted_msg):
    # message = msg.decode(FORMAT)
    msg_length = len(encrypted_msg)
    # Convert length to string, encode it, and pad to HEADER
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # pad with spaces
    client.send(send_length)  # send the length first
    client.send(encrypted_msg)      # then send the actual message

    # if msg in ["Hello", "Hi", "Asselema"]:
    #     reply = client.recv(2048).decode(FORMAT)
    #     print(f"[SERVER REPLY]: {reply}")
    # elif msg =="Goodbye" :
    #     reply=client.recv(2048).decode(FORMAT)
    #     print(f"[Tip]: {reply}")
    # elif msg == "help":
    #     reply=client.recv(2048).decode(FORMAT)
    #     print("Hello | Hi | Asselema : saluate the Server \ndisconnect : disconnecting from the Server")
    # else : 
    #     reply=client.recv(2048).decode(FORMAT)
    #     print(reply)
    
def encryption(msg):
    encrypted_data=cipher.encrypt(msg.encode(FORMAT))
    return( encrypted_data)
def decryption(msg):
    return(cipher.decrypt(msg).decode(FORMAT))

while True : 
    msg=str(input("Give me your message!"))
    if msg!= DISCONNECTmsg : 
        send(encryption(msg)) 
        break
encrypted_msg=encryption(msg)
send(encrypted_msg)