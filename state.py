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
            id = item[-1]
        # if action == 'add':
            price = float(item[-4])
            qty = item[-3]
            total_price = float(item[-2])
            product_type = item[-9]
        # check if it exist
        if details.get(id):
            existing = True
        # add product  
        if not existing and action == 'add':
            products.append(item)
            p_id,s_id = id.split('-')
            proto = {'product_id': None,'top_id':None,
                     'suit_id':None,'foot_wear_id':None,
                     'size_id':s_id,'qty':qty,
                     'unit_price':price,
                    'total_price':total_price,
                    'mini_price':price,
                    'expected_price':price * qty,
                    'p_group':pgroup,
                    'product_type':product_type
                        }
            proto[f'{pgroup}_id'] = p_id
            details[id] = proto
        # update 
        if existing and action == 'update':
            details[id]['qty'] = qty
            details[id]['unit_price'] = price
            details[id]['total_price'] = total_price
            details[id]['expected_price'] = details[id]['mini_price'] * details[id]['qty']
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
    
def proccess_sales(action='get'):
    if action == 'get':
        state = read_json('state.json')
        total = 0
        expected_price = 0
        
        items = []
        for key,value in state['cart']['products_meta'].items():
            items.append(value)
            expected_price += value['expected_price']
        for key,value in state['cart']['cart_totals'].items():
            total+=value
        
            
        data={'customer':state['customer'],
              'items': items,'total':total,
              'expected_price':expected_price,
              'branch':state['branch']
              }
        return data
        
        