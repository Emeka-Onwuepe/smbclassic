import sqlite3
import requests
from credit_sales.model import Credit_Sales, Payment

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

for key,model_ in  models.items():
    url = f'{base}api/getall?model={key}'

    re = requests.get(url)
    m2m = []
    data = re.json()
    for item in data['data']:
     
        item[f'{key}_id'] = item.pop('id')
        if key == 'product_type':
            item['category_id'] = item.pop('category')
        elif key == 'size':
            item['product_type_id'] = item.pop('product_type')
        elif key in ['product','suit','top','foot_wear']:
            item['product_type_id'] = item.pop('product_type')
            # for size in item['sizes']:  
            m2m = item.pop('sizes')
            
        instance  = model_(**item)
        instance.add_instance(con)
        
        for size_id in m2m:
            instance.add_m2m(con,size_id)
    

# try:
#     Customer.create_table(cur)
# except sqlite3.OperationalError as e:
#     print(e)


# con.close()

