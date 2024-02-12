import connection

def clean_up_database(table,ids):
    string = ''
    index = 0
    last = len(ids) - 1
    for id in ids:
        if index < last:
            string+=f'?,'
        else:
            string+=f'?'
        index += 1
    querry = f'''
            DELETE FROM {table}
            WHERE {table}_id NOT IN ({string})
            '''
    connection.cur.execute(querry,ids)
    
    if table not in ['size','category','product_type']:
        querry =  f'''
                    DELETE FROM {table}_sizes
                    WHERE {table}_id NOT IN ({string})
                    '''
        connection.cur.execute(querry,ids)
        
    if table == 'size':
        m2m_tables = ['suit_sizes','product_sizes',
                      'top_sizes','foot_wear_sizes']
        
        for m2m in  m2m_tables:
            querry =  f'''
                    DELETE FROM {m2m}
                    WHERE size_id NOT IN ({string})
                    '''
            connection.cur.execute(querry,ids)
            
    
    connection.con.commit()