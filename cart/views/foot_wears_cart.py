import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from state import get_products, update_cart
from statics import tree_height,frame_pady




class Foot_Wear_Cart_Treeview:
    add_to_cart = None

    def __init__(self,frame,grand_total):
        self.frame = frame
        self.grand_total = grand_total
        self.foot_wear_frame = ttkb.LabelFrame(self.frame,width=1360,text='Foot Wears Cart')
        self.foot_wear_frame.pack(pady=frame_pady)
     
        self.columns = ['type','brand','color','gender','age_group',
                        'sole_color',
                        'product_type','category','size','mini_price','pgroup',
                        'price','qty','total','id'
                        ]
        self.tree = ttkb.Treeview(self.foot_wear_frame,columns=self.columns,
                                  height=tree_height,
                                  bootstyle='dark',
                                 show='headings')
        self.tree.pack()
        controls = ttkb.LabelFrame(self.foot_wear_frame,text='controls')
        controls.pack()
        remove_buttton =  ttkb.Button(controls,text='Remove',
                                          command = self.delete_from_cart,
                                          bootstyle=DANGER).pack(side=LEFT,padx=30)
        
        update_frame = ttkb.LabelFrame(controls,text='Update')
        update_frame.pack(padx=10,pady=10)
        ttkb.Label(update_frame,text="Price").pack(side='left',padx=10,pady=10)
        self.price_value = ttkb.DoubleVar()
        self.price_input = ttkb.Entry(update_frame,textvariable=self.price_value,width=30)
        self.price_input.pack(side=LEFT,padx=10,pady=10)
        ttkb.Label(update_frame,text="Qty").pack(side='left',padx=10,pady=10)
        self.qty_value = ttkb.IntVar()
        self.qty_input = ttkb.Entry(update_frame,textvariable=self.qty_value,width=30)
        self.qty_input.pack(side=LEFT,padx=10,pady=10)
        update_buttton =  ttkb.Button(update_frame,text='Update',
                                          command = self.update_data,
                                          bootstyle=SUCCESS).pack(padx=10,pady=10)
        
        self.tree.bind('<ButtonRelease-1>',self.get_selected)
        
        for col in self.columns:
            self.tree.heading(col,text=col)
            self.tree.column(col,width=74,anchor=CENTER)
            
        Foot_Wear_Cart_Treeview.add_to_cart = self.add_data
        
        data = get_products('foot_wear')
        self.add_data(data,True)
        self.toggle()
        
        
    def toggle(self):
        items = self.tree.get_children()
        if items:
            self.foot_wear_frame.pack(pady=frame_pady)
        else:
            self.foot_wear_frame.pack_forget()
      
    def get_selected(self,e):
        id = self.tree.focus()
        values = self.tree.item(id,'values') 
        price = values[-4]
        qty = values[-3]
        self.qty_value.set(qty)
        self.price_value.set(price)
         
        
                
    def add_data(self,data,from_state =False):
        refined = []
        for item in data:
            if not from_state:
                price = item[-4]
                item = [*item[:-4],*item[-3:-2],price,item[-2],price,1,price,item[-1]]
                refined.append(item)
            self.tree.insert('',END,values=item,iid=item[-1])
        self.updateCart(refined)
        self.toggle()
        if not from_state and refined:
            txt = 'Product(s) added'
            Messagebox.ok(txt)
            
        
            
    def update_data(self):
        id = self.tree.focus()
        values = self.tree.item(id,'values') 
        price = self.price_input.get()
        price = float(price)
        qty = self.qty_input.get()
        qty = int(qty)
        item = [*values[:-4],price,qty,price*qty,values[-1]]
        self.tree.item(id,text="",values=item)
        self.qty_value.set(0)
        self.price_value.set(0)
        self.updateCart([item],'update')

    def delete_from_cart(self):
        txt = 'Are you sure you want to remove this product from cart?'
        result = Messagebox.okcancel(txt)
        if result == "Cancel":
            return
        data = []
        for record in self.tree.selection():
            self.tree.delete(record)
            data.append(record)
        self.qty_value.set(0)
        self.price_value.set(0)
        self.updateCart(data,'remove')
        self.toggle()
        
    def updateCart(self,product=[],action='add'):
        foot_wear_total = 0
        ids = self.tree.get_children()
        for id in ids:
            values = self.tree.item(id,'values')
            foot_wear_total += float(values[-2])
        grand_total = update_cart('foot_wear',foot_wear_total,product,action)
        self.grand_total.config(text=grand_total)
        
    def delete_all(self):
        for record in self.tree.get_children():
            self.tree.delete(record)
        grand_total = update_cart('foot_wear',0,[],'update')
        self.grand_total.config(text=grand_total)
        self.toggle()