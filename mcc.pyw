from Tkinter import *
import socket
import sys
import thread
import threading
            
class rcv(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        app.txt.insert(END, "Ready To Recieve\n")
        while True:
            data = self.conn(1024)
            app.txt.insert(END, "\n" + str(data),'l')
            


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 12330
s.connect((host,port))
class msngr:
    def __init__(self,wind):
        self.txt = Text(wind)
        self.msz = Entry(wind,width=100)
        snd = Button(wind,text="Send")
        self.txt.grid(columnspan=2)
        self.msz.grid(row=1)
        snd.grid(row=1,column=1)
        snd.bind("<Button-1>",self.show)
        self.txt.tag_configure('c',justify='right')
        self.txt.tag_configure('l',justify='left')
        self.txt.insert(END, "Connecting...\n")
        thread.start_new_thread(self.test,())
        

    def test(self):
        self.connected()

    def connected(self):
        self.txt.insert(END, "Connected: " + "\nWelcome\n")
        app.txt.insert(END, "Ready To Send\n")
        mr = rcv(s.recv)
        mr.start()
    
    def show(self,event):
        
        rep = app.msz.get()
        app.msz.delete(0,END)
        s.send(rep)
        self.txt.insert(END, "\nClient: "+rep,'c')

root = Tk()
app = msngr(root)
root.mainloop()
