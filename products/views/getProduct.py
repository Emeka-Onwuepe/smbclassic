import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from products.model import Product_Class
from qurried.models import Querried_Foot_Wear, Querried_Product, Querried_Product_Class, Querried_Suit, Querried_Top
from state import read_json, write_json
pgroup_ = read_json('state.json','pgroup')
gender_ = read_json('state.json','gender')
age_group_ = read_json('state.json','age_group')
import json


# <input type="text" name="type" id="type" required>
# <label for="color">Color</label>
# <input type="text" name="color" id="color" required>

models = {
          'product':Querried_Product,
          'suit':Querried_Suit,
          'top':Querried_Top,
          'foot_wear':Querried_Foot_Wear,
          }

class GetProductForm:

    def __init__(self,frame,cursor,suit_tree,*args, **kwargs):
        # frame = ttkb.Frame(app,borderwidth=10,style='light')
        frame.grid(row=0,column=0,pady=10,padx=5)
        self.cursor = cursor
        self.suit_tree = suit_tree
        pgroup_label = ttkb.Label(frame,text="P_Group").grid(row=1,column=0,pady=5,padx=5)
        self.pgroup = ttkb.Combobox(frame,values=pgroup_,width=40)
        self.pgroup.grid(row=1,column=1,pady=5,padx=5)
        
        gender_label = ttkb.Label(frame,text="Gender").grid(row=2,column=0,pady=5,padx=5)
        self.gender = ttkb.Combobox(frame,values=gender_,width=40)
        self.gender.grid(row=2,column=1,pady=5,padx=5)
        
        age_group_label = ttkb.Label(frame,text="Age_Group").grid(row=3,column=0,pady=5,padx=5)
        self.age_group = ttkb.Combobox(frame,values=age_group_,width=40)
        self.age_group.grid(row=3,column=1,pady=5,padx=5)
        
        product_type_label = ttkb.Label(frame,text="Product_Type").grid(row=4,column=0,pady=5,padx=5)
        self.product_type = ttkb.Entry(frame,width=40)
        self.product_type.grid(row=4,column=1,pady=5,padx=5)
        
        brand_label = ttkb.Label(frame,text="Brand").grid(row=5,column=0,pady=5,padx=5)
        self.brand = ttkb.Entry(frame,width=40)
        self.brand.grid(row=5,column=1,pady=5,padx=5)
        
        type_label = ttkb.Label(frame,text="Type").grid(row=6,column=0,pady=5,padx=5)
        self.type = ttkb.Entry(frame,width=40)
        self.type.grid(row=6,column=1,pady=5,padx=5)
        
        color_label = ttkb.Label(frame,text="Color").grid(row=7,column=0,pady=5,padx=5)
        self.color = ttkb.Entry(frame,width=40)
        self.color.grid(row=7,column=1,pady=5,padx=5)
        
        get_product_button =  ttkb.Button(frame,text='Get Product',
                                          command = self.get_product,
                                          bootstyle=SUCCESS).grid(row=8,column=0,columnspan=2,pady=5,padx=5)
 
    def get_product(self):
        data = {'type':self.type.get().strip(),'brand':self.brand.get().strip(),
                'color':self.color.get().strip(),'gender':self.gender.get().strip(),
                'age_group':self.age_group.get().strip(),'product_type':self.product_type.get().strip()}
        data = {'type': 'normal', 'brand': 'GB', 'color': 'Red', 'gender': 'U', 'age_group': 'A', 'product_type': 'First Turkish'}
        pgroup = self.pgroup.get().strip()
        pgroup = 'suit'
        products = Product_Class.get_product(self.cursor,pgroup,data)
        
        # product_type_id,suit_id,size_id
        need_data = []
        for product in products: 
            product = models[pgroup](*product,pgroup)
            values = list(product.__dict__.values())
            
            need_data.append(values) 
            # edited_data = [*product,pgroup] 
            
        self.suit_tree.add_data(need_data)        
        
        # # print(product.items())
        # data = json.dumps(product)
        # print()
        # product_type_id,suit_id,size_id  
            # Querried_Product_Class.suits.append(product)
        # write_json(need_data,'state.json','q_suits')
        
            
