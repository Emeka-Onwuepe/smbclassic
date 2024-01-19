import sqlite3
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

# try:
#     Customer.create_table(cur)
# except sqlite3.OperationalError as e:
#     print(e)


# con.close()