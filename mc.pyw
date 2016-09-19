from Tkinter import *
import socket
import sys
import thread
import threading

l = []
           
class rcv(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        app.txt.insert(END, "Ready To Recieve\n")
        while True:
            
            try:
                data = self.conn[0].recv(1024)
                app.txt.insert(END, "\nClient: " +str(self.conn[1])+": "+str(data),'l')
                for c in l:
                    if c!=self.conn:
                        c[0].send("Client: "+str(self.conn[1])+": "+str(data))
            except Exception as e:
                l.remove(self.conn)
                m = "\nClient"+str(self.conn[1])+" Disconnected"
                app.txt.insert(END, m+"\n")
                for c in l:
                    if c!=self.conn:
                        c[0].send(m)
                break

host=socket.gethostname()
port=12330
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))



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
        self.txt.insert(END, "Ready To Connect\n")
        thread.start_new_thread(self.test,())
        

    def test(self):
        while True:
            s.listen(5)
            self.c = s.accept()
            l.append(self.c)
            self.connected()

    def connected(self):
        self.txt.insert(END, "\nConnection From: " + str(self.c[1]) + "\nWelcome\n")
        app.txt.insert(END, "Ready To Send\n")
        mr = rcv(self.c)
        mr.start()
    
    def show(self,event):
        rep = app.msz.get()
        app.msz.delete(0,END)
        self.txt.insert(END, "\nServer: "+rep,'c')
        if(rep != ""):
            for c in l:
                try: 
                    c[0].send("Server: "+rep)
                except:
                    l.remove(c)
                

root = Tk()
app = msngr(root)
root.mainloop()
