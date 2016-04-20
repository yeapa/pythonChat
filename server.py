import socket
import sys
import threading

condition = threading.Condition()
HOST = raw_input("input the server's ip adrress: ") # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
data = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
s.bind((HOST, PORT))
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientThreadIn(cliSock, nick):
    global data
#infinite loop so that function do not terminate and thread do not end.
    while True:
    #Receiving from client
        try:
            temp = cliSock.recv(1024)
            if not temp:
                cliSock.close()
                return
            NotifyAll(temp)
            print data
        except:
            NotifyAll(nick + " leaves the room!")
            print data
            return

    #came out of loop

def NotifyAll(string):
    global data
    if condition.acquire():
        data = string
        condition.notifyAll()
        condition.release()

def clientThreadOut(cliSock, nick):
    global data
    while True:
        if condition.acquire():
            condition.wait()
            if data:
                try:
                    cliSock.send(data)
                    condition.release()
                except:
                    condition.release()
                    return

while 1:
    print "begin"
    #wait to accept a connection - blocking call
    cliSock, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    nick = cliSock.recv(1024)
     #send only takes string
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    NotifyAll('Welcome ' + nick + ' to the room!')
    print data
    print str((threading.activeCount() + 1) / 2) + ' person(s)!'
    cliSock.send(data)
    threading.Thread(target = clientThreadIn , args = (cliSock, nick)).start()
    threading.Thread(target = clientThreadOut , args = (cliSock, nick)).start()

s.close()
