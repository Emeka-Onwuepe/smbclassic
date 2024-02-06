import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from statics import queried_tree_height,frame_pady

from cart.views.top_cart import Top_Cart_Treeview
class Top_Treeview:
    def __init__(self,frame):
        self.frame = frame
        top_frame = ttkb.LabelFrame(self.frame,width=1360,text='tops')
        top_frame.pack(pady=frame_pady)
        self.columns = ['type','brand','color','gender','age_group',
                        'sleeves',
                        'product_type','category','price',
                        'size','pgroup','id'
                        ]
        self.tree = ttkb.Treeview(top_frame,columns=self.columns,
                                  height=queried_tree_height,
                                  bootstyle='dark',
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
        Top_Cart_Treeview.add_to_cart(selected)
            
            
    def add_data(self,data):
        for record in self.tree.get_children():
            self.tree.delete(record)
        for item in data:
            self.tree.insert('',END,values=item,iid=item[-1])
            
