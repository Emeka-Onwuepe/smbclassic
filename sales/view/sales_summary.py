import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from credit_sales.model import Credit_Sales, Payment

from customer.models import Customer
from sales.model import Items, Sales
from state import manage_customer, proccess_sales, read_json, write_json 
import json
import requests

from datetime import datetime 
from random import random
import math

# con = sqlite3.connect('database.db')
# cur = con.cursor()     
p_methods = read_json('state.json','payment_methods')

class Sales_Summary:
    
    def __init__(self,frame,con, *args, **kwargs):
        self.frame = frame
        self.con = con
        self.cursor = self.con.cursor()
        self.data = {'sales':[],
                     'credit_sales':[],
                     'payments':[]} 
        frame_1=ttkb.LabelFrame(frame,borderwidth=10,text='Credit Sales')
        frame_1.grid(row=0,column=0,pady=5,padx=5)
        frame_2=ttkb.LabelFrame(frame,borderwidth=10,text=' Payment')
        frame_2.grid(row=0,column=1,pady=5,padx=5)
        frame_3=ttkb.LabelFrame(frame,borderwidth=10,text='Sales')
        frame_3.grid(row=1,column=0,pady=5,padx=5)
        frame_4=ttkb.LabelFrame(frame,borderwidth=10,text='Transmit')
        frame_4.grid(row=1,column=1,pady=5,padx=5)
        
        # credit_sales
        self.credit_sales_columns = ['Customer','Phone Number','Amount','Date']
        self.credit_sales_tree = ttkb.Treeview(frame_1,columns=self.credit_sales_columns,bootstyle='dark',
                                 show='headings')
        self.credit_sales_tree.grid(row=0,column=0,pady=5,padx=5)
        for col in self.credit_sales_columns:
            self.credit_sales_tree.heading(col,text=col)
            self.credit_sales_tree.column(col,width=150,anchor=CENTER)
             
        # payment
        self.payment_columns = ['Customer','Phone Number','Amount','Date']
        self.payment_tree = ttkb.Treeview(frame_2,columns=self.payment_columns,bootstyle='dark',
                                 show='headings')
        self.payment_tree.grid(row=0,column=0,pady=5,padx=5)
        for col in self.payment_columns:
            self.payment_tree.heading(col,text=col)
            self.payment_tree.column(col,width=150,anchor=CENTER)
            
        
        # sales
        self.sales_columns = ['Date','Payment method',' Total Amount']
        self.sales_tree = ttkb.Treeview(frame_3,columns=self.sales_columns,bootstyle='dark',
                                 show='headings')
        self.sales_tree.grid(row=0,column=0,pady=5,padx=5)
        for col in self.sales_columns:
            self.sales_tree.heading(col,text=col)
            self.sales_tree.column(col,width=150,anchor=CENTER)
            
        # login and submit
        ttkb.Label(frame_4,text="Email:").grid(row=0,column=0,padx=5,pady=5)
        self.email = ttkb.Entry(frame_4,width=40)
        self.email.grid(row=0,column=1,padx=5,pady=5)
        ttkb.Label(frame_4,text="Password:").grid(row=1,column=0,padx=5,pady=5)
        self.password = ttkb.Entry(frame_4,width=40,show='*')
        self.password.grid(row=1,column=1,padx=5,pady=5)
        ttkb.Button(frame_4,text="Submit",command = self.submit_data,
                                          bootstyle=SUCCESS).grid(
                                                            row=2,column=0,
                                                            columnspan=2,
                                                            pady=5
                                                        )
        
        # get stats  
        self.add_sales()
        self.add_credit_sales()
        self.add_payments()
        
        # prepare data
        self.prepare_date()
 
    def add_sales(self):
        for record in self.sales_tree.get_children():
            self.sales_tree.delete(record)
        data = Sales.get_summary(self.cursor)
        for item in data:
            self.sales_tree.insert('',END,values=item)
    
    def add_credit_sales(self):
        data = Credit_Sales.get_summary(self.cursor)
        for item in data:
            self.credit_sales_tree.insert('',END,values=item)
       
    
    def add_payments(self):
        for record in self.payment_tree.get_children():
            self.payment_tree.delete(record)
        data = Payment.get_summary(self.cursor)
        for item in data:
            self.payment_tree.insert('',END,values=item)
            
    def prepare_date(self):
        sales_data = []
        credit_sales_data = []
        payments_data = []
        credit_sales_id = read_json('state.json','credit_sales')
        # branch = read_json('state.json','branch')
        sales = Sales.get_sales(self.cursor)
        credit_sales = Credit_Sales.get_credit_sales(self.cursor,credit_sales_id)
        payments = Payment.get_payments(self.cursor)
        # prepare sales
        for sale in sales:
            data = sale[:-4]
            customer = sale[-4:]
            sale = Sales(*data)
            items = Items.get_items(self.cursor,'sales',sale.sales_id)
            sale = sale.__dict__
            sale['orders'] = []
            # sale['branch_id'] = branch['id']
            sale['phone_number'] = customer[0]
            sale['email'] = customer[1]
            sale['name'] = customer[2]
            sale['address'] = customer[3]
            
            for item in items:
                item = Items(*item[:-2])
                sale['orders'].append(item.__dict__)
            sales_data.append(sale)
        # prepare credit sales
        for sale in credit_sales:
            sale = list(sale)
            sale.pop(1)
            data = sale[:-4]
            customer = sale[-4:]
            sale = Credit_Sales(*data)
            items = Items.get_items(self.cursor,'credit',sale.credit_sales_id)
            sale = sale.__dict__
            sale['phone_number'] = customer[0]
            sale['email'] = customer[1]
            sale['name'] = customer[2]
            sale['address'] = customer[3]
            sale['payment_method'] = 'credit'
            del sale['p_total_amount']
            sale['orders'] = []
            # sale['branch_id'] = branch['id']
            for item in items:
                item = Items(*item[:-2])
                item = item.__dict__
                sale['orders'].append(item)
            credit_sales_data.append(sale)
            
        # prepare payments
        for payment in payments:
            id = payment[0]
            payment = Payment(*payment[1:])
            payment = payment.__dict__
            payment['id'] = id
            payments_data.append(payment)
        
        self.data = {'sales':sales_data,
                     'credit_sales':credit_sales_data,
                     'payments':payments_data}  
        
    def submit_data(self):
        credit_sales_id = read_json('state.json','credit_sales')
        logged = False
        reset = True
        base = 'http://127.0.0.1:8000/api/'

        login_data = {"email":'pascalemy2010@gmail.com',
                      'password':'casdonmystery1959'}
        url = base + 'login'
        login_data = json.dumps(login_data)
        headers= { 'Content-Type': 'application/json'}
        login = requests.post(url,data=login_data,headers=headers)
        if login.status_code == 200:
            logged =True
            user = login.json()
            headers['Authorization'] = f"Token {user['token']}"
        
        if not logged:
            return
        for item in self.data['sales']:
            url = base + 'process'
            data  = json.dumps(item)
            re = requests.post(url,data,headers=headers)
            if re.status_code == 200:
                Sales.delete_sale(self.con,item['sales_id'])
                self.add_sales()
            else:
                reset = False
            
        
        for item in self.data['credit_sales']:
            url = base + 'process'
            data  = json.dumps(item)
            re = requests.post(url,data,headers=headers)
            if re.status_code == 200:
                credit_sales_id.pop(credit_sales_id.index(item['credit_sales_id']))
                write_json(credit_sales_id,'state.json','credit_sales')
                Credit_Sales.delete_credit_sale(self.con,item['credit_sales_id'])
            else:
                reset = False
                
        for item in self.data['payments']:
            url = base + 'creditpayment'
            data  = json.dumps(item)
            re = requests.post(url,data,headers=headers)
            if re.status_code == 200:
                data = re.json()
                Payment.delete_instance(self.con,data['id'])
                self.add_payments()
                
        if reset:
            write_json(0,'state.json','sales_id')
            write_json(0,'state.json','item_id')
    