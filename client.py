#-*-coding:utf-8-*-
import socket
import threading
from Tkinter import *
import datetime
import time
import sys
outString=''
mutex = threading.Lock()
class Client(object):
    """docstring for ClientView"""
    def __init__(self):
        self.nick = "hello1"
        self.ip ="localhost"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, 8888))
        self.sock.send(self.nick)
        self.root = Tk()
        self.root.title('chatting with xxx')
        self.frame_left_top   = Frame(width=380, height=270, bg='white')
        self.frame_left_center  = Frame(width=380, height=100, bg='white')
        self.frame_left_bottom  = Frame(width=380, height=20)
        self.frame_right     = Frame(width=170, height=400, bg='white')
        ##创建需要的几个元素
        self.text_msglist    = Text(self.frame_left_top)
        # print "flag",self.text_msglist
        self.text_msg      = Text(self.frame_left_center)
        self.text_friend      = Text(self.frame_right)
        # button_sendmsg   = Button(frame_left_bottom, text='发送', command=sendMessage)
        #创建一个绿色的tag
        self.text_msglist.tag_config('green', foreground='#008B00')
        #使用grid设置各个容器位置
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_left_center.grid(row=1, column=0, padx=2, pady=5)
        self.frame_left_bottom.grid(row=2, column=0)
        self.frame_right.grid(row=0, column=1, rowspan=3,padx=4, pady=5)
        self.frame_left_top.grid_propagate(0)
        self.frame_left_center.grid_propagate(0)
        self.frame_left_bottom.grid_propagate(0)
        self.frame_right.grid_propagate(0)
        #把元素填充进frame
        self.text_msglist.grid()
        self.text_msg.grid()
        self.text_friend.grid(ipadx=50)
        self.button_sendmsg   = Button(self.frame_left_bottom, text='发送',command=self.send)
        self.button_sendmsg.grid(sticky=E)
        thin = threading.Thread(target =self.receive)
        thin.start()
        self.showView()

    def showView(self):
        self.root.mainloop()

    def send(self):
        #在聊天内容上方加一行 显示发送人及发送时间
        global outString
        outString = self.nick + ': ' + self.text_msg.get('0.0', END)
        self.sock.send(outString)
        msgcontent = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n '
        self.text_msglist.insert(END, msgcontent, 'green')
        self.text_msglist.insert(END, self.text_msg.get('0.0', END))
        self.text_msg.delete('0.0', END)

    def receive(self):
        global outString
        while True:
            try:
                inString = self.sock.recv(1024)
                if not inString:
                    break
                print inString
                if inString!=outString:
                    pass
                    print inString
                    self.text_msglist.insert(END,inString,'green')
                    self.text_msglist.update()

            except:
                break

client=Client()
