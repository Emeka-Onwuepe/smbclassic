import sqlite3
import requests
from clean_up_db import clean_up_database
from credit_sales.model import Credit_Sales, Payment
from state import read_json, write_json
branch = read_json('state.json','branch')


from customer.models import Customer
from products.model import (Category, Foot_Wear, 
                            Product, Product_Type, Size, Suit, Top)
from sales.model import Items, Sales
con = sqlite3.connect('database.db')
cur = con.cursor()

models = [Customer,Category,Product_Type,Size,
          Product,Suit,Top,Foot_Wear,Items,
          Sales,Credit_Sales,Payment
          ]
# create tables
for model in models:
    model.create_table(cur)
    
models = {'category':Category,
          'product_type':Product_Type,
          'size':Size,
          'product':Product,
          'suit':Suit,
          'top':Top,
          'foot_wear':Foot_Wear,
          'customer':Customer
          }

base = 'http://127.0.0.1:8000/'

# get data one
def get_data():
    try:
        returned_ids = {'category':[],
                        'product_type':[],
                        'size':[],
                        'product':[],
                        'suit':[],
                        'top':[],
                        'foot_wear':[]
                        }
        
        for key,model_ in  models.items():
            url = f'{base}api/getall?model={key}'
                   
            re = requests.get(url)
            m2m = []
            data = re.json()
            for item in data['data']:
                if key != 'customer':
                    returned_ids[key].append(item['id'])
                item[f'{key}_id'] = item.pop('id')
                
                if key == 'product_type':
                    item['category_id'] = item.pop('category')
                elif key == 'size':
                    item['product_type_id'] = item.pop('product_type')
                elif key in ['product','suit','top','foot_wear']:
                    item['product_type_id'] = item.pop('product_type')
                    m2m = item.pop('sizes')
                    
                if key in ['product','suit','top','foot_wear']:
                    # delete non returned products
                    pass
                    if m2m:
                        pass
                    # delete non returned size ids
               
                   
                instance  = model_(**item)
                instance.add_instance(con,update=True)
                

                
                for size_id in m2m:
                    instance.add_m2m(con,size_id,update=True)
        # clean the database
        for key,value in returned_ids.items():
            if value:
                clean_up_database(key,value)
        
        if type(branch['id']) == str:
            url = f'{base}api/getbranch?name={branch["name"]}'
            re = requests.get(url)
            data = re.json()
            branch['id'] = data['id']
            write_json(branch,'state.json','branch')
            
    except requests.exceptions.ConnectionError:
        return 0
    return 1
    
