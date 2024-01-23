import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import connection
from products.views.getProduct import GetProductForm
from qurried.models import Querried_Product_Class
from qurried.views.queried_suits import Suit_Treeview
from sales.view.sales import Sales_Detail
from state import read_json

querried = {'suit':[]}

app = ttk.Window(themename='journal',)
app.title('SMBClassic Sale and Stock App')
# app.iconbitmap('logo.png')
# app.iconphoto('logo.png')
# app.geometry('1400x1000')

main_frame = ttk.Frame(app,borderwidth=5)
main_frame.pack()

get_product_frame = ttk.Frame(main_frame,borderwidth=10,padding=65,style='light')
# get_product_frame.pack()


customer_frame = ttk.Frame(main_frame,borderwidth=10,style='light')
# customer_frame.pack()

suit_tree = Suit_Treeview(app)
form = GetProductForm(get_product_frame,connection.cur,suit_tree)
Sales_Detail(customer_frame,connection.cur)
# GetProductForm(customer_frame)
# def check():
#     read_json()
    
# check_button =  ttk.Button(main_frame,text='Check',
#                                           command = check,
#                                     bootstyle=SUCCESS)



app.mainloop()
