# TO DO 1: connect to ftp and send the text file over
# TO DO 2: Loop through folder and send a sequence to ftp 

from tkinter import *
from tkinter import filedialog
from tkinter import StringVar
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os

#192.168.10.10 u=Test p =password 
import pync
from ftplib import FTP

#Connect to FTP 
class myFTP():
	def __init__(self):
		ftp = None#FTP(None)
		 
	def connectFTP(self,path = '.',ftp_ip ='192.168.10.10',ftp_user = 'Test',ftp_password = 'password',ftp_to_directory = '/sai/'):
		ftp = FTP(ftp_ip)#'192.168.10.10' 
		ftp.login(user=ftp_user, passwd = ftp_password) #user='Test', passwd = 'password'
		ftp.cwd(ftp_to_directory) #'/sai/'
		pync.notify('connecting to ' + ftp_ip , title='Python FTP app')
# 		#Hack. directly using placeFile here instead of using the function
		filename = open(GUI.watch_path + '/v001/screenshot.png','rb')
		print(filename)
		
		ftp.storbinary('STOR screenshot.png',filename)#ftp.storbinary('STOR '+filename,open(filename, 'rb'))
		ftp.quit()
# 		localfile.close()
# 		pync.notify('downloaded' + filename + 'from FTP' , title='Python FTP app') 
		
		

# download file
# 	def grabFile(self,someFile):
# 		filename = someFile
# 		localfile = open(filename, 'wb')
# 		ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
# 		ftp.quit()
# 		localfile.close()
# 		pync.notify('downloaded' + filename + 'from FTP' , title='Python FTP app')
# 
# upload file
# 	def placeFile(self,someFile):
# 		filename = someFile #exampleFile.txt
# 		ftp.storbinary('STOR '+filename, open(filename, 'rb'))
# 		ftp.quit()
# 		pync.notify('uploaded' + filename + 'to FTP' , title='Python FTP app')

class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path='.', patterns=['*.txt','*.pdf'], logfunc=print):#patterns='*'
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)#recursive = false means dont go through subfolders
        self.log = logfunc
        self.my_ftp = '.'
   
    def on_created(self, event):
        # This function is called when a file is created
        if event.src_path.lower().endswith('.txt'):
        	self.log(f"hey, {event.src_path} has been created!")
        	self.my_ftp = myFTP()# Connect to FTP
        	
        	
 
    def on_deleted(self, event):
        # This function is called when a file is deleted
        self.log(f"what the f**k! Someone deleted {event.src_path}!")
 
    def on_modified(self, event):
        # This function is called when a file is modified
        if event.src_path.lower().endswith('.txt'):
        	self.log(f"hey buddy, {event.src_path} has been modified")
 
    def on_moved(self, event):
        # This function is called when a file is moved    
        self.log(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
 
class GUI:
    watch_path = None
    def __init__(self):
        self.watchdog = None
        self.watch_patterns ='*.pdf'
        self.root = Tk()
        self.messagebox = Text(width=80, height=10)
        self.messagebox.pack()
        frm = Frame(self.root)
        
        #Create FTP object
        self.my_ftp = '.'
        
        self.StringVar1 = StringVar()
        
        self.path= '.'
        
        self.entry_feild = Entry(self.root,textvariable = self.StringVar1) #self.entry_feild = Entry(self.root,textvariable = self.StringVar1)
        self.entry_feild.pack()

        Button(frm, text='Browse', command=self.select_path).pack(side=LEFT)
        Button(frm, text='Start FTP', command=self.start_ftp).pack(side=RIGHT)
        Button(frm, text='Stop Watchdog', command=self.stop_watchdog).pack(side=RIGHT)
        Button(frm, text='Start Watchdog', command=self.start_watchdog).pack(side=RIGHT)

        frm.pack(fill=X, expand=1)
        self.root.mainloop()
       
    def start_watchdog(self):
        if self.watchdog is None:
            self.watchdog = Watchdog(path=self.path,logfunc=self.log)
            print('Watchdog path is :' + self.path )
            print('watch_path is :' + GUI.watch_path)
            self.watchdog.start()
            self.log('Watchdog started')
        else:
            self.log('Watchdog already started')
           
    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log('Watchdog stopped')
        else:
            self.log('Watchdog is not running')
   
    def select_path(self):
        self.path = filedialog.askdirectory()
        if self.path:
            GUI.watch_path = self.path
            print('path variable is ' + self.path)
            print('watch_path variable is ' + GUI.watch_path)
            self.StringVar1.set(self.path)
            self.log(f'Selected path: {self.path}')
   
    def log(self, message):
        self.messagebox.insert(END, f'{message}\n')
        self.messagebox.see(END)
        
    def start_ftp(self):
        self.my_ftp = myFTP()
        print(self.path) 
        self.my_ftp.connectFTP(GUI.watch_path)
#         self.messagebox.see(END)
       
if __name__ == '__main__': #GUI() class is created and run only if this python file is opened inside terminal  
    GUI() #if this python file is imported inside another python file, the GUI class will not be run 