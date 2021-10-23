import socket

Server_IP= input("연결할 server의 ip를 입력하십시오: ")
PORT = int(input("연결할 server의 PORT를 입력하십시오: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Server_IP, PORT))

while True:
    msg  =  str(input("-> "))
    if msg =='q':
        client_socket.close()

    data = msg.encode()

    length = len(data)

    client_socket.sendall(length.to_bytes(4,byteorder="little"))

    client_socket.sendall(data)

    data = client_socket.recv(4)

    length = int.from_bytes(data, "little")

    data = client_socket.recv(length)

    msg = data.decode()

    print('Received from Server: ', msg)
    
