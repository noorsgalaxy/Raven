from Tkinter import *
import socket
import sys
import thread
import threading
            
class rcv(threading.Thread):
    def run(self):
        app.txt.insert(END, "Ready To Recieve\n")
        while True:
            data = s.recv(1024)
            app.txt.insert(END, "\n" + str(data),'l')
            


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 12330

class msngr:
    def __init__(self,wind):
        self.txt = Text(wind)
        self.msz = Entry(wind,width=100)
        snd = Button(wind,text="Send")
        cnnct = Button(wind,text="Connect",command=self.enter_name)
        self.txt.grid(columnspan=2)
        self.msz.grid(row=1)
        snd.grid(row=1,column=1)
        cnnct.grid(row=2)
        
        snd.bind("<Button-1>",self.show)
        self.txt.tag_configure('c',justify='right')
        self.txt.tag_configure('l',justify='left')
        self.txt.insert(END, "Connecting...\n")
        
##        thread.start_new_thread(self.test,())
        
    def enter_name(self):
        self.namew = Toplevel(root)
        label_name = Label(self.namew,text="Enter Your Name")
        self.entry_name = Entry(self.namew)
        self.button_name = Button(self.namew,text="OK",command=self.test)
        label_name.pack()
        self.entry_name.pack()
        self.button_name.pack()

    def test(self):
        self.n = self.entry_name.get()
        self.namew.destroy()
        self.connected()
##        thread.start_new_thread(self.connected,())

    def connected(self):
        s.connect((host,port))
        s.send(str(self.n))
        print self.n
        self.txt.insert(END, str(self.n)+" You are Connected: " + "\nWelcome\n")
        app.txt.insert(END, "Ready To Send\n")
        mr = rcv()
        mr.start()
    
    def show(self,event):
        
        rep = app.msz.get()
        app.msz.delete(0,END)
        s.send(rep)
        self.txt.insert(END, "\nClient: "+rep,'c')

root = Tk()
app = msngr(root)
root.mainloop()
