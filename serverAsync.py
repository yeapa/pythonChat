import socket
import sys
import select


def broadcast_data(sock, message):
    for socket in connectList:
        if socket != sockServer and socket != sock:
            try:
                socket.send(data)
            except:
                socket.close()
                connectList.remove(socket)


ip = "127.0.0.1"
port = 8888
connectList = []
sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sockServer.bind((ip, port))
except socket.error as e:
    print(e)
    sys.exit()
sockServer.listen(5)
connectList.append(sockServer)
print("socket start at %s : %d" % (ip, port))

while 1:
    read_sockets, write_sockets, error_sockers = select.select(connectList, [], [])
    for socket in read_sockets:
        if socket == sockServer:
            sock_client, addr_client = sockServer.accept()
            connectList.append(sock_client)
            print("client %s:%s is connected" % addr_client)
            broadcast_data(sock_client, "%s:%s  enter the room" % addr_client)
        else:
            try:
                data = socket.recv(2048)
                if data:
                    broadcast_data(socket, data)
            except:
                broadcast_data(socket, "a client is offline")
                socket.close()
                connectList.remove(socket)

sockServer.close()