import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from cart.views.suit_cart import Suit_Cart_Treeview
class Suit_Treeview:
    def __init__(self,frame):
        self.frame = frame
        suit_frame = ttkb.LabelFrame(self.frame,width=1360,text='Suits')
        suit_frame.pack()
        self.columns = ['type','brand','color','gender','age_group',
                        'breasted','button','pics','golden_button',
                        'product_type','category','price',
                        'size','pgroup','id'
                        ]
        self.tree = ttkb.Treeview(suit_frame,columns=self.columns,bootstyle='dark',
                                 show='headings')
        self.tree.pack()
        
        add_to_cart_button  =  ttkb.Button(frame,text='Add to Cart',
                                          command = self.add_to_cart,
                                          bootstyle=SUCCESS).pack()
        for col in self.columns:
            self.tree.heading(col,text=col)
            self.tree.column(col,width=90,anchor=CENTER)
    
    def add_to_cart(self):
        selected = []
        ids = self.tree.selection()
        for id in ids:
            item = self.tree.item(id,'values')
            selected.append(item)
        Suit_Cart_Treeview.add_to_cart(selected)
            
            
    def add_data(self,data):
        for record in self.tree.get_children():
            self.tree.delete(record)
        for item in data:
            self.tree.insert('',END,values=item,iid=item[-1])
            
