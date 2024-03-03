import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttkb
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *
import pandas as pd
from state import api_base, df_to_list
import json
import requests


class Upload_page:
    
    def __init__(self,frame,*args, **kwargs):
        self.frame = frame
        # self.con = con
        # self.cursor = self.con.cursor
        self.file_location= ''
        self.file_type = ''
        frame_1=ttkb.LabelFrame(frame,borderwidth=10,text='Data Upload',padding=40)
        frame_1.pack(pady=40)
        ttkb.Label(frame_1,text="Action:").grid(row=0,column=0,pady=5,padx=5)
        self.action = ttkb.Combobox(frame_1,values=['Add Stock','Add Product'],width=40)
        self.action.grid(row=0,column=1,pady=5,padx=5)
        ttkb.Label(frame_1,text="Branch:").grid(row=1,column=0,padx=5,pady=5)
        self.branch = ttkb.Entry(frame_1,width=40)
        self.branch.grid(row=1,column=1,pady=5,padx=5)
        ttkb.Button(frame_1,text="Select File",command=self.get_file).grid(row=2,column=0,padx=5,pady=5)
        self.file =  ttkb.Label(frame_1, text='No file selected',width=40)
        self.file.grid(row=2,column=1,pady=5,padx=5)
        ttkb.Label(frame_1,text="Email:").grid(row=3,column=0,padx=5,pady=5)
        self.email = ttkb.Entry(frame_1,width=40)
        self.email.grid(row=3,column=1,padx=5,pady=5)
        ttkb.Label(frame_1,text="Password:").grid(row=4,column=0,padx=5,pady=5)
        self.password = ttkb.Entry(frame_1,width=40,show='*')
        self.password.grid(row=4,column=1,padx=5,pady=5)
        ttkb.Button(frame_1,text="Submit", command=self.upload,
                                          bootstyle=SUCCESS).grid(
                                                            row=5,column=0,
                                                            columnspan=2,
                                                            pady=5
                                                        )

    def get_file(self):
        file_name = filedialog.askopenfilename(filetypes=[('csv file','*.csv'),('Excel File','*.xlsx')])
        self.file_location = file_name
        self.file_type = self.file_location.split('.')[-1]
        self.file.config(text=self.file_location.split('/')[-1])
        
    def upload(self):
        logged = False
        base = api_base
        
        data_available = False
        if self.file_location:
            data_available = True
            
        if not data_available:
            self.email.delete(0,END)
            self.password.delete(0,END)
            Messagebox.ok('No data to send')
            return
        
        login_data = {"email":self.email.get().strip(),
                      'password':self.password.get().strip()}
        
        url = base + 'login'
        login_data = json.dumps(login_data)
        headers= { 'Content-Type': 'application/json'}
        login = None
        try:
            login = requests.post(url,data=login_data,headers=headers)
        except requests.exceptions.ConnectionError:
            Messagebox.ok('Connection error')
        if login.status_code == 200:
        
            user = login.json()
            headers['Authorization'] = f"Token {user['token']}"
            if user['user']['is_admin']:
                logged =True
        
       
                
        if not self.action.get().strip():
            Messagebox.ok('Please Select Action')
            return
                
        if self.action.get().strip() == 'Add Stock':
            if not self.branch.get().strip():
                Messagebox.ok('Please add branch') 
                return
        if logged:
            if self.file_type == 'csv':
                data = pd.read_csv(self.file_location)
            else:
                data = pd.read_excel(self.file_location)
                
        if not logged:
            Messagebox.ok('Access Denied')
            return
             
        json_data = {'data':df_to_list(data),
                    }
        json_data = json.dumps(json_data)
        # send data
                    #  'branch': self.branch.get().strip(),
        if self.action.get().strip() == 'Add Product':
            url = base + 'addproduct'
            data  = json_data
            re = requests.post(url,data,headers=headers)
            if re.status_code == 200:
                Messagebox.ok(re.json()['status'])
            else:
                print(re.text)
                
        if self.action.get().strip() == 'Add Stock':
            pass
            
        
        self.email.delete(0,END)
        self.password.delete(0,END)
        
        
        
        