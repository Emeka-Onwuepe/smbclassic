import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from cart.views.suit_cart import Suit_Cart_Treeview
import connection
from products.views.getProduct import GetProductForm
from qurried.views.queried_suits import Suit_Treeview
from sales.view.sales import Sales_Detail
from ttkbootstrap.scrolled import ScrolledFrame
from state import read_json

querried = {'suit':[]}

app = ttkb.Window(themename='superhero',)
app.title('SMBClassic Sale and Stock App')
# app.iconbitmap('logo.png')
# app.iconphoto('logo.png')
# app.geometry('1400x1000')

# scroll = ttkb.Scrollbar(app,orient='vertical')
# scroll.pack(side='right',fill='y')

# main frame
main_frame = ScrolledFrame(app,borderwidth=5,height=830,width=1400)
main_frame.pack()

# scroll.config()


# structure

frame_1 = ttkb.Frame(main_frame,borderwidth=10,)
frame_1.pack()
frame_2 = ttkb.Frame(main_frame,borderwidth=10)
frame_2.pack()
frame_3 = ttkb.Frame(main_frame,borderwidth=10)
frame_3.pack()
# frame_1 = ttkb.Frame(app,borderwidth=10)



get_product_frame = ttkb.LabelFrame(frame_2,borderwidth=10,padding=65,text="Get Product")
# get_product_frame.pack()


sales_frame = ttkb.LabelFrame(frame_2,borderwidth=10,text='Record Sale')
# customer_frame.pack()

suit_cart = Suit_Cart_Treeview(frame_1)
suit_tree = Suit_Treeview(frame_3)
form = GetProductForm(get_product_frame,connection.cur,suit_tree)
Sales_Detail(sales_frame,connection.cur)
# GetProductForm(customer_frame)
# def check():
#     read_json()
    
# check_button =  ttkb.Button(main_frame,text='Check',
#                                           command = check,
#                                     bootstyle=SUCCESS)



app.mainloop()
