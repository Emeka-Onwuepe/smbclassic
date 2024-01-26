import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from cart.views.suit_cart import Suit_Cart_Treeview
# from ttkbootstrap.scrolled import ScrolledFrame

class Suit_Treeview:
    def __init__(self,frame):
        self.frame = frame
        # self.suit_cart = suit_cart
        suit_frame = ttkb.LabelFrame(self.frame,width=1360,text='Suits')
        # tree_frame = ttkb.Frame(self.frame,width=1360,)
        suit_frame.pack()
        # self.columns = ['type','brand','description','color','gender','age_group',
        #                 'product_type_id','breasted','button','pics','golden_button',
        #                 'suit_id','product_type','size_id','category','price',
        #                 'size','pgroup','id'
        #                 ]
        self.columns = ['type','brand','color','gender','age_group',
                        'breasted','button','pics','golden_button',
                        'product_type','category','price',
                        'size','pgroup','id'
                        ]
        # self.columns = ['type','brand']
        self.tree = ttkb.Treeview(suit_frame,columns=self.columns,bootstyle='success',
                                 show='headings')
        self.tree.tag_configure('even',background='lightgreen')
        self.tree.pack()
        # self.tree['columns'] = self.columns
        
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
        count = 0
        for item in data:
            # if count % 2 == 0:
            self.tree.insert('',END,values=item,iid=item[-1])
            # else:
            #    self.tree.insert('',END,values=item,iid=item[-1]) 
            # count +=1
