import math

def mrp(part_name, req, day, bom, stock):
    lt, ss, ls = bom[part_name]['params']
    
    net = max(0, req + ss - stock.get(part_name, 0))
    ordered = math.ceil(net / ls) * ls
    release_day = day - lt
    
    stock[part_name] = stock.get(part_name, 0) + ordered - req
    print(f"[{part_name}] Zamów: {ordered} na dzień: {release_day} (potrzeba: {req})")

    for child, qty in bom[part_name].get('children', []):
        mrp(child, ordered * qty, release_day, bom, stock)

data = {
    'Rower': {'params': (1, 0, 1), 'children': [('Rama', 1), ('Kolo', 2)]},
    'Rama':  {'params': (3, 2, 5), 'children': []},
    'Kolo':  {'params': (2, 5, 10), 'children': [('Szprycha', 36)]},
    'Szprycha': {'params': (1, 50, 100), 'children': []}
}

print("Harmonogram MRP:")
mrp('Rower', 10, 15, data, {'Rama': 3, 'Kolo': 2, 'Szprycha': 20})