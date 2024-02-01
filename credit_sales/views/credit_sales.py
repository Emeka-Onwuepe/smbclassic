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
from credit_sales.model import Credit_Sales, Payment


from state import manage_customer, proccess_sales, read_json, write_json 

from datetime import datetime 


# con = sqlite3.connect('database.db')
# cur = con.cursor()     
p_methods = read_json('state.json','payment_methods')

class Credit_Sales_Detail:
    
    def __init__(self,frame,con, *args, **kwargs):
        self.frame = frame
        self.con = con
        self.cursor = self.con.cursor()
        self.customer_phone_number = None
        self.phone_string = ttkb.StringVar()
        self.amount_string = ttkb.DoubleVar()
        self.edit_amount_string = ttkb.DoubleVar()
        
        frame_1=ttkb.LabelFrame(frame,borderwidth=10,text='Get Customer')
        frame_1.grid(row=0,column=0,pady=5,padx=5)
        phone_number_label_ = ttkb.Label(frame_1,text="Phone_Number").grid(row=1,column=0,pady=5,padx=5)
        self.phone = ttkb.Entry(frame_1,width=40,textvariable=self.phone_string)
        self.phone.grid(row=1,column=1,pady=5,padx=5)
        get_customer_button =  ttkb.Button(frame_1,text='Get Customer',
                                          command = self.get_customer,
                                          bootstyle=SUCCESS).grid(row=2,column=0,
                                                                  columnspan=2,
                                                                  pady=5,padx=5)
                                          
        frame_2 = ttkb.LabelFrame(frame,borderwidth=10,text='Credit Sales') 
        frame_2.grid(row=0,column=1,pady=5,padx=5)                             
        self.columns = ['Purchase Id','Total Amount','Total Payment',
                        'Expected Price','Balance','credit_sales_id'
                        ]
        
        self.tree = ttkb.Treeview(frame_2,columns=self.columns,bootstyle='dark',
                                 show='headings')
        self.tree.grid(row=0,column=0,pady=5,padx=5)
        
        for col in self.columns:
            self.tree.heading(col,text=col)
            self.tree.column(col,width=150,anchor=CENTER)
            
        self.tree.bind('<ButtonRelease-1>',self.get_selected)
        
        frame_3=ttkb.LabelFrame(frame,borderwidth=10,text='Add payment')
        frame_3.grid(row=1,column=0,pady=5,padx=5)
        ttkb.Label(frame_3,text="Purchase_id: ").grid(row=0,column=0,pady=5,padx=5)
        self.purchase_id = ttkb.Label(frame_3,text="")
        self.purchase_id.grid(row=0,column=1,pady=5,padx=5)
        amount_label_ = ttkb.Label(frame_3,text="Amount").grid(row=1,column=0,pady=5,padx=5)
        self.amount = ttkb.Entry(frame_3,width=40,textvariable=self.amount_string)
        self.amount.grid(row=1,column=1,pady=5,padx=5)
        add_payment_button =  ttkb.Button(frame_3,text='Add payment',
                                          command = self.add_payment,
                                          bootstyle=SUCCESS).grid(row=2,column=0,
                                                                  columnspan=2,
                                                                  pady=5,padx=5)
                                          
        frame_4 = ttkb.LabelFrame(frame,borderwidth=10,text='Credit Sales payments') 
        frame_4.grid(row=1,column=1,pady=5,padx=5)                             
        self.columns_ = ['Purchase Id','Amount','Date','Id']
        
        self.payment_tree = ttkb.Treeview(frame_4,columns=self.columns_,bootstyle='dark',
                                 show='headings')
        self.payment_tree.grid(row=1,column=1,pady=5,padx=5)
        
        for col in self.columns_:
            self.payment_tree.heading(col,text=col)
            self.payment_tree.column(col,width=150,anchor=CENTER)
            
        self.payment_tree.bind('<ButtonRelease-1>',self.get_selected_payment)
        
        frame_5=ttkb.LabelFrame(frame,borderwidth=10,text='Edit payment')
        frame_5.grid(row=2,column=0,pady=5,padx=5)
        ttkb.Label(frame_5,text="id: ").grid(row=0,column=0,pady=5,padx=5)
        self.id = ttkb.Label(frame_5,text="")
        self.id.grid(row=0,column=1,pady=5,padx=5)
        amount_label_ = ttkb.Label(frame_5,text="Amount").grid(row=1,column=0,pady=5,padx=5)
        ttkb.Entry(frame_5,width=40,textvariable=self.edit_amount_string).grid(row=1,column=1,pady=5,padx=5)
        ttkb.Button(frame_5,text='Edit Payment',
                                          command = self.edit_payment,
                                          bootstyle=SUCCESS).grid(row=2,column=0,
                                                                #   columnspan=2,
                                                                  pady=5,padx=5)
        ttkb.Button(frame_5,text='Delete Payment',
                                          command = self.delete_payment,
                                          bootstyle=DANGER).grid(row=2,column=1,
                                                                #   columnspan=2,
                                                                  pady=5,padx=5)
 
    def get_selected_payment(self,e):
        self.purchase_id['text'] = ''
        id = self.payment_tree.focus()
        values = self.payment_tree.item(id,'values') 
        self.id['text']= values[-1]
        self.edit_amount_string.set(values[1])
    
    def get_selected(self,e):
        self.id['text'] = ''
        self.edit_amount_string.set(0.0)
        id = self.tree.focus()
        values = self.tree.item(id,'values') 
        self.purchase_id['text']= values[0]
        
         
    def get_customer(self,from_class=False):
       credit_sales = Credit_Sales.get_customer_credits(self.cursor,'08132180216')
       self.customer_phone_number = '08132180216'
       payments = Payment.get_instance(self.cursor,'08132180216',True)
       data = []
       for credit in credit_sales:
           needed = [credit.purchase_id,credit.total_amount,credit.total_payment,
                  credit.expected_price,credit.balance,credit.credit_sales_id]
           data.append(needed)
       self.add_data(data)
    #    payments
       data = []
       for payment in payments:
           needed = [payment.purchase_id,payment.amount,payment.date,payment.id]
           data.append(needed)
       self.add_payment_data(data)
                               
    def add_data(self,data):
        for record in self.tree.get_children():
            self.tree.delete(record)
        for item in data:
            self.tree.insert('',END,values=item,iid=item[0])
            
    def add_payment_data(self,data):
        for record in self.payment_tree.get_children():
            self.payment_tree.delete(record)
        for item in data:
            self.payment_tree.insert('',END,values=item,iid=item[-1])
        
 
    def add_payment(self):
        selected = self.tree.focus()
        values = self.tree.item(selected,'values')
        amount = self.amount_string.get()
        data = {'credit_sales_id':values[-1],'amount':amount,
                'date':datetime.now().strftime("%d/%b/%Y %H:%M"),'purchase_id':values[0]
                }
        payment = Payment(**data)
        payment.add_instance(self.con)
        Credit_Sales.update_instance(self.con,amount,values[0])
        self.get_customer(True)
        self.amount_string.set(0.0)
        self.purchase_id['text'] = ''
        
    def edit_payment(self):
        
        selected = self.payment_tree.focus()
        values = self.payment_tree.item(selected,'values')
        prev_amount = values[1]
        
        id = int(self.id['text'])
        amount = self.edit_amount_string.get()
        
        Payment.update_instance(self.con,amount,id)
        
        diff = amount - float(prev_amount)
        
        Credit_Sales.update_instance(self.con,diff,values[0])
        
        self.get_customer(True)
        self.id['text'] = ''
        self.edit_amount_string.set(0.0)
        
    def delete_payment(self):
        selected = self.payment_tree.focus()
        values = self.payment_tree.item(selected,'values')
        amount = float(values[1]) * -1
        Credit_Sales.update_instance(self.con,amount,values[0])
        id = int(self.id['text'])
        Payment.delete_instance(self.con,id)
        
        
        self.get_customer(True)
        self.id['text'] = ''
        self.edit_amount_string.set(0.0)

        
                