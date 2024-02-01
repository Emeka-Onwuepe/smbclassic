import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from cart.views.suit_cart import Suit_Cart_Treeview
import connection
from credit_sales.views.credit_sales import Credit_Sales_Detail
from products.views.getProduct import GetProductForm
from qurried.views.queried_suits import Suit_Treeview
from sales.view.sales import Sales_Detail
from ttkbootstrap.scrolled import ScrolledFrame
# from state import read_json

querried = {'suit':[]}

app = ttkb.Window(themename='superhero',)
app.title('SMBClassic Sale and Stock App')
# app.iconbitmap('logo.png')
# app.iconphoto('logo.png')
# app.geometry('1400x1000')

# scroll = ttkb.Scrollbar(app,orient='vertical')
# scroll.pack(side='right',fill='y')

# main frame

main_frame = ScrolledFrame(app,height=830,width=1400)
main_frame.pack()
nav = ttkb.Frame(main_frame)
nav.pack()
ttkb.Button(nav,text="Sales",command=lambda : mainPage()).pack(side=LEFT,padx=10,pady=10)
ttkb.Button(nav,text="Sales Summary",command=lambda : summaryPage()).pack(side=LEFT,padx=10,pady=10)
ttkb.Button(nav,text="Credit Sales",command=lambda : creditSalePage()).pack(side=LEFT,padx=10,pady=10)
wrapper = ttkb.Frame(main_frame)
wrapper = ttkb.Frame(main_frame)

wrapper.pack()

def summaryPage():
    
    for fn in wrapper.winfo_children():
        fn.destroy()
    app.update()
        
    ttkb.Label(wrapper,text='Sales Summary').pack()

def creditSalePage():
    
    for fn in wrapper.winfo_children():
        fn.destroy()
    app.update()
    Credit_Sales_Detail(wrapper,connection.con)
        


def mainPage():
     
    for fn in wrapper.winfo_children():
        fn.destroy()
    app.update()
    frame_1 = ttkb.Frame(wrapper,borderwidth=10,)
    frame_1.pack()
    total_details = ttkb.Frame(frame_1)
    total_details.pack(side=BOTTOM)
    ttkb.Label(total_details,text="Grand Total:").pack(side=LEFT)
    grand_total = ttkb.Label(total_details,text="0")
    grand_total.pack(side=LEFT)
    suit_cart = Suit_Cart_Treeview(frame_1,grand_total)
    frame_2 = ttkb.Frame(wrapper,borderwidth=10)
    frame_2.pack()
    frame_3 = ttkb.Frame(wrapper,borderwidth=10)
    frame_3.pack()
    get_product_frame = ttkb.LabelFrame(frame_2,borderwidth=10,padding=65,text="Get Product")
    sales_frame = ttkb.LabelFrame(frame_2,borderwidth=10,text='Record Sale')
    suit_tree = Suit_Treeview(frame_3)
    form = GetProductForm(get_product_frame,connection.cur,suit_tree)
    Sales_Detail(sales_frame,connection.con,[suit_cart])
    
    
mainPage()
app.mainloop()
