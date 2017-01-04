import socket
import sys
import select


def prompt():
    sys.stdout.write('<you>')
    sys.stdout.flush()

if len(sys.argv) < 2:
    print("please use this script like clientAsync.py name")
    sys.exit()
name = sys.argv[1]
ip = 'localhost'
try:
    sockSer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print(e)
    sys.exit()
sockSer.connect((ip, 8888))

prompt()
while 1:
    socket_list = [sys.stdin, sockSer]
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for socket in read_sockets:
        if socket == sockSer:
            data = socket.recv(4096)
            if not data:
                print("disconnected from chat server")
                sys.exit()
            else:
                sys.stdout.write(data)
                prompt()
        else:
            msg = sys.stdin.readline()
            sockSer.send(msg)
            prompt()
