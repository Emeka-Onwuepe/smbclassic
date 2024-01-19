import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import connection
from customer.models import Customer
from state import read_json

branch = read_json('state.json','branch')
print(branch)

    
customer = Customer('Emeka Onwu','080090900','pppp','fff')
customer.add_instance(connection.con)

customer = Customer('james','0800900','pppp','fff')
customer.add_instance(connection.con)
r_customer = Customer.get_instance(connection.cur,"0800900")
print(r_customer)
app = tk.Tk()
app.title('SMBClassic Sale and Stock App')

# b1 = ttk.Button(app, text="Button 1", bootstyle=SUCCESS)
# b1.pack(side=LEFT, padx=5, pady=10)

# b2 = ttk.Button(app, text="Button 2", bootstyle=(INFO, OUTLINE))
# b2.pack(side=LEFT, padx=5, pady=10)

app.mainloop()
