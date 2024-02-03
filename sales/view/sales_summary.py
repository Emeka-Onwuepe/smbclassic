import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from credit_sales.model import Credit_Sales, Payment

from customer.models import Customer
from sales.model import Items, Sales
from state import manage_customer, proccess_sales, read_json, write_json 

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
                     'payment':[]} 
        frame_1=ttkb.LabelFrame(frame,borderwidth=10,text='Sales')
        frame_1.grid(row=0,column=0,pady=5,padx=5)
        frame_2=ttkb.LabelFrame(frame,borderwidth=10,text=' Credit Sales')
        frame_2.grid(row=0,column=1,pady=5,padx=5)
        frame_3=ttkb.LabelFrame(frame,borderwidth=10,text='Payments')
        frame_3.grid(row=1,column=0,columnspan=2,pady=5,padx=5)
        
        # sales
        self.sales_columns = ['Date','Payment method',' Total Amount']
        self.sales_tree = ttkb.Treeview(frame_1,columns=self.sales_columns,bootstyle='dark',
                                 show='headings')
        self.sales_tree.grid(row=0,column=0,pady=5,padx=5)
        for col in self.sales_columns:
            self.sales_tree.heading(col,text=col)
            self.sales_tree.column(col,width=150,anchor=CENTER)
            
        # credit_sales
        self.credit_sales_columns = ['Customer','Phone Number','Amount','Date']
        self.credit_sales_tree = ttkb.Treeview(frame_2,columns=self.credit_sales_columns,bootstyle='dark',
                                 show='headings')
        self.credit_sales_tree.grid(row=0,column=0,pady=5,padx=5)
        for col in self.credit_sales_columns:
            self.credit_sales_tree.heading(col,text=col)
            self.credit_sales_tree.column(col,width=150,anchor=CENTER)
             
        # payment
        self.payment_columns = ['Customer','Phone Number','Amount','Date']
        self.payment_tree = ttkb.Treeview(frame_3,columns=self.payment_columns,bootstyle='dark',
                                 show='headings')
        self.payment_tree.grid(row=0,column=0,pady=5,padx=5)
        for col in self.payment_columns:
            self.payment_tree.heading(col,text=col)
            self.payment_tree.column(col,width=150,anchor=CENTER)
        
        # get stats  
        self.add_sales()
        self.add_credit_sales()
        self.add_payments()
        
        # prepare data
        self.prepare_date()
        
    def add_sales(self):
        data = Sales.get_summary(self.cursor)
        for item in data:
            self.sales_tree.insert('',END,values=item)
    
    def add_credit_sales(self):
        data = Credit_Sales.get_summary(self.cursor)
        for item in data:
            self.credit_sales_tree.insert('',END,values=item)
       
    
    def add_payments(self):
        data = Payment.get_summary(self.cursor)
        for item in data:
            self.payment_tree.insert('',END,values=item)
            
    def prepare_date(self):
        sales_data = []
        credit_sales_data = []
        payments_data = []
        credit_sales_id = read_json('state.json','credit_sales')
        sales = Sales.get_sales(self.cursor)
        credit_sales = Credit_Sales.get_credit_sales(self.cursor,credit_sales_id)
        payments = Payment.get_payments(self.cursor)
        # prepare sales
        for sale in sales:
            sale = Sales(*sale)
            items = Items.get_items(self.cursor,'sales',sale.sales_id)
            sale = sale.__dict__
            sale['items'] = []
            for item in items:
                item = Items(*item[:-2])
                sale['items'].append(item.__dict__)
            sales_data.append(sale)
        # prepare credit sales
        for sale in credit_sales:
            sale = list(sale)
            sale.pop(1)
            sale = Credit_Sales(*sale)
            items = Items.get_items(self.cursor,'credit',sale.credit_sales_id)
            sale = sale.__dict__
            del sale['p_total_amount']
            sale['items'] = []
            for item in items:
                item = Items(*item[:-2])
                item = item.__dict__
                sale['items'].append(item)
            credit_sales_data.append(sale)
        # prepare payments
        for payment in payments:
            payment = Payment(*payment)
            payments_data.append(payment.__dict__)
        
        self.data = {'sales':sales_data,
                     'credit_sales':credit_sales_data,
                     'payment':payments_data}  
        
