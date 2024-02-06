import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from statics import queried_tree_height,frame_pady

from cart.views.foot_wears_cart import Foot_Wear_Cart_Treeview
class Foot_Wear_Treeview:
    def __init__(self,frame):
        self.frame = frame
        foot_wear_frame = ttkb.LabelFrame(self.frame,width=1360,text='foot_wears')
        foot_wear_frame.pack(pady=frame_pady)
        self.columns = ['type','brand','color','gender','age_group',
                        'sole_color',
                        'product_type','category','price',
                        'size','pgroup','id'
                        ]
        self.tree = ttkb.Treeview(foot_wear_frame,columns=self.columns,
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
        Foot_Wear_Cart_Treeview.add_to_cart(selected)
            
            
    def add_data(self,data):
        for record in self.tree.get_children():
            self.tree.delete(record)
        for item in data:
            self.tree.insert('',END,values=item,iid=item[-1])
            
