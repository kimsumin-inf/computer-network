
import socket
import sys
import threading


def binding(client_socket, addr):
    print("conneted by", addr)

    try:
        while True:
            data= client_socket.recv(4)

            length = int.from_bytes(data, "little")

            data =client_socket.recv(length)

            msg = data.decode()

            print("메세지 도착")
            print(f"from {addr} :", msg)

            msg = str(input("-> "))
            
            data= msg.encode()

            length= len(data)

            client_socket.sendall(length.to_bytes(4,byteorder="little"))

            client_socket.sendall(data)

            


    except:
        print("except: ", addr)
        
    finally:
        client_socket.close()






print("this program 내부 통신용")
HOST = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST)
print(f"HOST name: {HOST},\nHOST_IP: {HOST_IP}")
PORT = int(input("Server에서 사용할 PORT를 입력하십시요: "))

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST_IP,PORT))

server_socket.listen(1) # 클라이언트의 연결 받을 수 있는 상태



try:
    while True:
        client_socket, addr = server_socket.accept()
        th = threading.Thread(target=binding, args=(client_socket,addr))
        th.start()

except:
    print("server")
   

finally:
    server_socket.close()