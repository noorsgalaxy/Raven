from Tkinter import *
import socket
import sys
import thread
import threading

l = []
d = {}
cd = {}
class rcv(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        while True:
            
            
            data = self.conn[0].recv(1024)
##                assert(data!="")
                           
            app.txt.insert(END,"\n"+str(cd[self.conn])+": "+str(data),'l')
            
            if ' @' in data:
                n = data[data.index(' @')+2:]
                data = data[:data.index(' @')]
                    #if c!=self.conn and c == d[n]:
                d[n][0].send(str(cd[self.conn])+": "+str(data))
            else:
                for c in l:
                    if c!=self.conn:
                        c[0].send(str(cd[self.conn])+": "+str(data))
##            except Exception as e:
##                l.remove(self.conn)
##                print e
##                m = "\nClient"+str(self.conn[1])+" Disconnected"
##                app.txt.insert(END, m+"\n")
##                for c in l:
##                    c[0].send(m)
##                break

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
            data = self.c[0].recv(1024)
            d[data] = self.c
            cd[self.c] = data
            print d
            l.append(self.c)
            self.connected()

    def connected(self):
        self.txt.insert(END, "\nConnection From: " + cd[self.c])
        for c in l:
            c[0].send("Server: "+cd[self.c]+" Joined The Chat")
##        app.txt.insert(END, "Ready To Send\n")
        mr = rcv(self.c)
        mr.start()
    
    def show(self,event):
        rep = app.msz.get()
        app.msz.delete(0,END)
        
        if(rep != ""):
            self.txt.insert(END, "\nServer: "+rep,'c')
            if ' @' in rep:
                n = rep[rep.index(' @')+2:]
                rep = rep[:rep.index(' @')]
                    #if c!=self.conn and c == d[n]:
                d[n][0].send("Server: "+rep)                
            else:
                for c in l:
                    c[0].send("Server: "+rep)
##            for c in l:
##                if n!='':
##                    if c!=self.conn and c == d[n]:
##                    c[0].send("Server: "+rep)
##                else:
##                    if c!=self.conn:
##                    c[0].send("Server: "+rep)
                    
root = Tk()
app = msngr(root)
root.mainloop()
