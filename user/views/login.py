import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

class Login_View:
    
    def __init__(self,frame,start_app, *args, **kwargs):
        frame = ttkb.LabelFrame(frame,borderwidth=10,text='Login')
        frame.pack(padx=150,pady=150)
        self.start_app = start_app
        ttkb.Label(frame,text="Email:").grid(row=0,column=0,padx=5,pady=5)
        self.email = ttkb.Entry(frame,width=40)
        self.email.grid(row=0,column=1,padx=5,pady=5)
        ttkb.Label(frame,text="Password:").grid(row=1,column=0,padx=5,pady=5)
        self.password = ttkb.Entry(frame,width=40,show='*')
        self.password.grid(row=1,column=1,padx=5,pady=5)
        ttkb.Button(frame,text="Submit",command = self.login,
                                          bootstyle=SUCCESS).grid(
                                                            row=2,column=0,
                                                            columnspan=2,
                                                            pady=5
                                                        )
                                          
    def login(self):
        self.start_app()