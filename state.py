import json


base = '.'

def get_location(name):
    return f"{base}/{name}"

def read_json(name,key=None):
    file_location = get_location(name)
    file_location = name
    # print(file_location)
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
    grand_toatl = 0
    totals = read_json('state.json','cart_totals')
    totals[pgroup] = total
    for key,value in totals.items():
        grand_toatl += value
    write_json(totals,'state.json','cart_totals')
    return grand_toatl
    