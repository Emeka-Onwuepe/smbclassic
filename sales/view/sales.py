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
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from customer.models import Customer
from state import read_json  

# con = sqlite3.connect('database.db')
# cur = con.cursor()     
p_methods = read_json('state.json','payment_methods')

class Sales_Detail:
    
    def __init__(self,frame,cursor, *args, **kwargs):
        self.frame = frame
        self.cursor = cursor
        self.frame.grid(row=0,column=1,pady=10,padx=5)
        # string vars
        self.name_string = ttk.StringVar()
        self.phone_string = ttk.StringVar()
        self.phone_number_string = ttk.StringVar()
        self.email_string = ttk.StringVar()
        self.address_string = ttk.StringVar()
        
        frame_1=ttk.Frame(frame,borderwidth=10,style='light')
        frame_1.grid(row=0,column=0,pady=5,padx=5)
        frame_2=ttk.Frame(frame,borderwidth=10,style='light')
        frame_2.grid(row=0,column=1,pady=5,padx=5)
        
      
        ttk.Label(frame_1,text='Get Customer',background='#FAFAFA',
                  font=("Arial",18,'bold')).grid(row= 0,column=0,columnspan=2)
        
        phone_number_label_ = ttk.Label(frame_1,text="Phone_Number",background='#FAFAFA').grid(row=1,column=0,pady=5,padx=5)
        self.phone = ttk.Entry(frame_1,width=40,textvariable=self.phone_string)
        self.phone.grid(row=1,column=1,pady=5,padx=5)
        get_customer_button =  ttk.Button(frame_1,text='Get Customer',
                                          command = self.get_customer,
                                          bootstyle=SUCCESS).grid(row=2,column=0,
                                                                  columnspan=2,
                                                                  pady=5,padx=5)
 
        
        ttk.Label(frame_2,text='Customer Details',background='#FAFAFA',
                  font=("Arial",18,'bold')).grid(row= 0,column=0,columnspan=2)
        
        name_label = ttk.Label(frame_2,text="Name",background='#FAFAFA').grid(row=1,column=0,pady=5,padx=5)
        self.name = ttk.Entry(frame_2,width=40,textvariable=self.name_string)
        self.name.grid(row=1,column=1,pady=5,padx=5)
        
        phone_number_label = ttk.Label(frame_2,text="Phone_Number",background='#FAFAFA').grid(row=2,column=0,pady=5,padx=5)
        self.phone_number = ttk.Entry(frame_2,width=40,textvariable=self.phone_number_string)
        self.phone_number.grid(row=2,column=1,pady=5,padx=5)
        
        email_label = ttk.Label(frame_2,text="Email",background='#FAFAFA').grid(row=3,column=0,pady=5,padx=5)
        self.email = ttk.Entry(frame_2,width=40,textvariable=self.email_string)
        self.email.grid(row=3,column=1,pady=5,padx=5)
        
        address_label = ttk.Label(frame_2,text="Address",background='#FAFAFA').grid(row=4,column=0,pady=5,padx=5)
        self.address = ttk.Entry(frame_2,width=40,textvariable=self.address_string)
        self.address.grid(row=4,column=1,pady=5,padx=5)
        
        payment_method_label = ttk.Label(frame_2,text="Payment_Method",background='#FAFAFA').grid(row=5,column=0,pady=5,padx=5)
        self.payment_method = ttk.Combobox(frame_2,values=p_methods,width=40)
        self.payment_method.grid(row=5,column=1,pady=5,padx=5)
        
        remark_label = ttk.Label(frame_2,text="Remark",background='#FAFAFA').grid(row=6,column=0,pady=5,padx=5)
        self.remark = ttk.Text(frame_2,width=40,height=10)
        self.remark.grid(row=6,column=1,pady=5,padx=5)
        
        get_sales_button =  ttk.Button(frame_2,text='Submit ',
                                          command = self.record_sales,
                                          bootstyle=SUCCESS).grid(row=7,column=0,
                                                                  columnspan=2,
                                                                  pady=5,padx=5)
        
    def get_customer(self):
        data = self.phone.get()
    
        customer = Customer.get_instance(self.cursor,data.strip())
        if customer:
            self.phone_number_string.set(customer.phone_number)
            self.name_string.set(customer.name)
            self.email_string.set(customer.email)
            self.address_string.set(customer.address)
            # self.phone_string.set('')
            # self.phone_string.set('')
            
            
    def record_sales(self):
        pass