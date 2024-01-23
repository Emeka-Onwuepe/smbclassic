import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

class Suit_Treeview:
    def __init__(self,frame):
        self.frame = frame
        tree_frame = ScrolledFrame(self.frame,width=1360,)
        tree_frame = ttk.Frame(self.frame,width=1360,)
        tree_frame.pack()
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
        self.tree = ttk.Treeview(tree_frame,bootstyle=SUCCESS,columns=self.columns,
                                 show='headings')
        self.tree.tag_configure('even',background='lightgreen')
        self.tree.pack()
        self.tree['columns'] = self.columns
        for col in self.columns:
            self.tree.heading(col,text=col)
            self.tree.column(col,width=90,anchor=CENTER)
        
            
    def add_data(self,data):
        for record in self.tree.get_children():
            self.tree.delete(record)
        count = 0
        for item in data:
            if count % 2 == 0:
                self.tree.insert('',END,values=item,iid=item[-1],tags=('even',))
            else:
               self.tree.insert('',END,values=item,iid=item[-1]) 
            count +=1
