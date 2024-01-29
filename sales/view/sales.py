#  <p><strong>Name:</strong> <a href="{% url 'credit_sales:creditSalesView' customer.id 'view' %}">{{customer.name}}</a></p>
#         <p><strong>Phone Number:</strong>  <a href="tel:{{customer.phone_number}}">{{customer.phone_number}}</a> </p>
#         <p><strong>Email:</strong> {{customer.email}}</p>
#         <p><strong>Address:</strong> {{customer.address}}</p>
#         <p><strong>Purchase_id:</strong> {{sale.purchase_id}}</p>
#         <p><strong>Payment_method:</strong> {% if sale.payment_method %} {{sale.payment_method}}{% else %} Credit {% endif %}</p>
#         <p><strong>Remark: </strong>{{sale.remark}}</p>
#         <p><strong>Date:</strong> {{sale.date}}</p>
#         <p><strong>Paid: </strong> {{sale.paid}} </p>
        
# import sqlite3
import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from customer.models import Customer
from sales.model import Items, Sales
from state import manage_customer, proccess_sales, read_json 

from datetime import datetime 
from random import random
import math

# con = sqlite3.connect('database.db')
# cur = con.cursor()     
p_methods = read_json('state.json','payment_methods')

class Sales_Detail:
    
    def __init__(self,frame,con, *args, **kwargs):
        self.frame = frame
        self.con = con
        self.cursor = self.con.cursor()
        self.frame.grid(row=0,column=1,pady=10,padx=5)
        # string vars
        self.name_string = ttkb.StringVar()
        self.phone_string = ttkb.StringVar()
        self.phone_number_string = ttkb.StringVar()
        self.email_string = ttkb.StringVar()
        self.address_string = ttkb.StringVar()
        
        frame_1=ttkb.LabelFrame(frame,borderwidth=10,text='Get Customer')
        frame_1.grid(row=0,column=0,pady=5,padx=5)
        frame_2=ttkb.LabelFrame(frame,borderwidth=10,text='Sales Details')
        frame_2.grid(row=0,column=1,pady=5,padx=5)
        
        phone_number_label_ = ttkb.Label(frame_1,text="Phone_Number").grid(row=1,column=0,pady=5,padx=5)
        self.phone = ttkb.Entry(frame_1,width=40,textvariable=self.phone_string)
        self.phone.grid(row=1,column=1,pady=5,padx=5)
        get_customer_button =  ttkb.Button(frame_1,text='Get Customer',
                                          command = self.get_customer,
                                          bootstyle=SUCCESS).grid(row=2,column=0,
                                                                  columnspan=2,
                                                                  pady=5,padx=5)
 
        
        name_label = ttkb.Label(frame_2,text="Name").grid(row=1,column=0,pady=5,padx=5)
        self.name = ttkb.Entry(frame_2,width=40,textvariable=self.name_string)
        self.name.grid(row=1,column=1,pady=5,padx=5)
        
        phone_number_label = ttkb.Label(frame_2,text="Phone_Number").grid(row=2,column=0,pady=5,padx=5)
        self.phone_number = ttkb.Entry(frame_2,width=40,textvariable=self.phone_number_string)
        self.phone_number.grid(row=2,column=1,pady=5,padx=5)
        
        email_label = ttkb.Label(frame_2,text="Email").grid(row=3,column=0,pady=5,padx=5)
        self.email = ttkb.Entry(frame_2,width=40,textvariable=self.email_string)
        self.email.grid(row=3,column=1,pady=5,padx=5)
        
        address_label = ttkb.Label(frame_2,text="Address").grid(row=4,column=0,pady=5,padx=5)
        self.address = ttkb.Entry(frame_2,width=40,textvariable=self.address_string)
        self.address.grid(row=4,column=1,pady=5,padx=5)
        
        payment_method_label = ttkb.Label(frame_2,text="Payment_Method").grid(row=5,column=0,pady=5,padx=5)
        self.payment_method = ttkb.Combobox(frame_2,values=p_methods,width=40)
        self.payment_method.grid(row=5,column=1,pady=5,padx=5)
        
        remark_label = ttkb.Label(frame_2,text="Remark").grid(row=6,column=0,pady=5,padx=5)
        self.remark = ttkb.Text(frame_2,width=40,height=10)
        self.remark.grid(row=6,column=1,pady=5,padx=5)
        
        get_sales_button =  ttkb.Button(frame_2,text='Submit ',
                                          command = self.record_sales,
                                          bootstyle=SUCCESS).grid(row=7,column=0,
                                                                  columnspan=2,
                                                                  pady=5,padx=5)
        self.get_customer(True)
        
    def get_customer(self,from_state=False):
        if from_state:
            customer = manage_customer('get')
            if customer:
                self.phone_number_string.set(customer['phone_number'])
                self.name_string.set(customer['name'])
                self.email_string.set(customer['email'])
                self.address_string.set(customer['address'])
        else:
            data = self.phone.get()
            customer = Customer.get_instance(self.cursor,data.strip())
            if customer:
                self.phone_number_string.set(customer.phone_number)
                self.name_string.set(customer.name)
                self.email_string.set(customer.email)
                self.address_string.set(customer.address)
                manage_customer('add',customer.__dict__) 
                           
        
    def record_sales(self):
        data = proccess_sales()
        customer = data['customer']
        items = data['items']
        total = data['total']
        branch = data['branch']['id']
        expected_price = data['expected_price']
        sales_id = data['sales_id']
        item_id =  data['item_id']
        
        date = datetime.now().microsecond
        random_ = math.floor(random()*100)
        bran = data['branch']['name'][:3]
        purchase_id = f'smb{bran}{random_}{date}'
        
        sales_id += 1
        
        sale = {'customer_id':customer['customer_id'], 'total_amount':total,
                 'logistics':0.0,"expected_price":expected_price,
                  'destination':'pick-up','remark':self.remark.get('1.0',END).strip(),
                   'channel':'store','payment_method':self.payment_method.get().strip(),
                   'date':datetime.now().strftime("%d/%b/%Y %H:%M"), 'purchase_id':purchase_id,
                   'paid':True,'branch':branch,
                    'sales_id': sales_id
                 }
        sales = Sales(**sale)
        sales.add_instance(self.con)
        for item in items:
            item_id += 1
            item = Items(*item.values(),item_id)
            item.add_instance(self.con,sales_id)
        
        # update sales_id
        # update item_id
        # clear customer
        # clear cart
        #  "cart": {"cart_totals": {"suit": 0, "product": 0, "foot_wear": 0, "top": 0}, "products_meta": {}, "products": []}
        
        
        # print(items)
        # print(customer)
                