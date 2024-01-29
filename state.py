import json


base = '.'

def get_location(name):
    return f"{base}/{name}"

def read_json(name,key=None):
    file_location = get_location(name)
    file_location = name
    try:
        with open(file_location,'r') as openfile:
            data = json.load(openfile)
            if key:
                return data[key]
            return data
    except (FileNotFoundError, KeyError)as e:
        if key:
            return []
        return {}

def write_json(data,name,key=None):
    file_location = get_location(name)
    if key:
        initial_data = read_json(name)
        initial_data[key] = data
        data = initial_data
    data = json.dumps(data)
    with open(file_location,'w') as outfile:
        outfile.write(data)

def update_total(pgroup,total):
    grand_total = 0
    totals = read_json('state.json','cart_totals')
    totals[pgroup] = total
    for key,value in totals.items():
        grand_total += value
    write_json(totals,'state.json','cart_totals')
    return grand_total
    
def update_cart(pgroup,total,product=[],action='add'):
    grand_total = 0
    cart = read_json('state.json','cart')
    
    totals = cart['cart_totals']
    details = cart['products_meta']
    products = cart['products']
    
    # update totals
    totals[pgroup] = total
    for key,value in totals.items():
        grand_total += value
       
    # update products and 
    # product metas 
    for item in product:
        existing = False
        price = 0
        total_price = 0
        qty = 0
        id = None
        if action == 'remove':
            id = item
        else:
            price = float(item[-4])
            qty = item[-3]
            total_price = float(item[-2])
            id = item[-1]
        # check if it exist
        if details.get(id):
            existing = True
        # add product  
        if not existing and action == 'add':
            products.append(item)
            p_id,s_id = id.split('-')
            details[id] = {'product_id':p_id,'size_id':s_id,
                           'qty':qty,'price':price,
                           'total': total_price,
                           'mini_price':price,
                           'pgroup':pgroup}
        # update 
        if existing and action == 'update':
            details[id]['qty'] = qty
            details[id]['price'] = price
            details[id]['total'] = total_price
        # delete
        if existing and action == 'remove':
            del details[id]
            products = [product for product in products if product[-1]!= id]
            
    cart = {'cart_totals':totals,
            'products_meta':details,
            'products':products}
    write_json(cart,'state.json','cart')
    return grand_total

def get_products(pgroup):
    cart = read_json('state.json','cart')
    products = cart['products']
    products = [product for product in products if product[-5]== pgroup]
    return products
    
    
def manage_customer(action='get',data={}):
    customer = read_json('state.json','customer')
    if action == 'get':
        return customer
    if action == 'add':
        write_json(data,'state.json','customer')
        return
    if action == 'remove':
        write_json({},'state.json','customer')
        return
    
        
        