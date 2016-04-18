#-*-coding:utf-8-*-
import socket
import threading
from Tkinter import *
import datetime
import time
import sys
def sendMessage(s):
    #在聊天内容上方加一行 显示发送人及发送时间
    global nick,outString
    outString = nick + ': ' + text_msg.get('0.0', END)
    s.send(outString)
    msgcontent = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n '
    text_msglist.insert(END, msgcontent, 'green')
    text_msglist.insert(END, text_msg.get('0.0', END))
    text_msg.delete('0.0', END)

def DealOut(s):
    global nick, outString
    while True:
        outString = raw_input(">")
        outString = nick + ': ' + outString
        s.send(outString)

def DealIn(s):
    global inString
    while True:
        try:
            inString = s.recv(1024)
            if not inString:
                break
            if outString != inString:
                print inString
        except:
            break

def main():
    root = Tk()
    root.title('chatting with xxx')

    inString = ''
    outString = ''
    nick = ''

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 8888))
    sock.send(nick)

    thin = threading.Thread(target = DealIn, args = (sock,))
    thin.start()
    thout = threading.Thread(target = sendMessage, args = (sock,))
    thout.start()

    ##界面
    #创建几个frame作为容器
    frame_left_top   = Frame(width=380, height=270, bg='white')
    frame_left_center  = Frame(width=380, height=100, bg='white')
    frame_left_bottom  = Frame(width=380, height=20)
    frame_right     = Frame(width=170, height=400, bg='white')
    ##创建需要的几个元素
    text_msglist    = Text(frame_left_top)
    text_msg      = Text(frame_left_center)
    text_friend      = Text(frame_right)
    button_sendmsg   = Button(frame_left_bottom, text='发送', command=sendMessage)
    #创建一个绿色的tag
    text_msglist.tag_config('green', foreground='#008B00')
    #使用grid设置各个容器位置
    frame_left_top.grid(row=0, column=0, padx=2, pady=5)
    frame_left_center.grid(row=1, column=0, padx=2, pady=5)
    frame_left_bottom.grid(row=2, column=0)
    frame_right.grid(row=0, column=1, rowspan=3,padx=4, pady=5)
    frame_left_top.grid_propagate(0)
    frame_left_center.grid_propagate(0)
    frame_left_bottom.grid_propagate(0)
    frame_right.grid_propagate(0)
    #把元素填充进frame
    text_msglist.grid()
    text_msg.grid()
    text_friend.grid(ipadx=50)
    button_sendmsg.grid(sticky=E)
    root.mainloop()

nick = raw_input("input your nickname: ")
ip = raw_input("input the server's ip adrress: ")
main()
#sock.close()
