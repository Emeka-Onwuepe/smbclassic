class Items:
    def __init__(self, 
                 product_id:int,top_id:int,
                 suit_id:int,foot_wear_id:int,
                 size_id:int,qty:int,
                 unit_price:float,
                 total_price:float,
                 mini_price:float,
                 expected_price:float,
                 p_group:str,
                 product_type:str,
                 items_id:int = 0
                 ):
       
        self.product_id = product_id
        self.top_id = top_id
        self.suit_id = suit_id
        self.foot_wear_id = foot_wear_id
        self.size_id = size_id
        self.qty = qty
        self.unit_price = unit_price
        self.total_price = total_price
        self.mini_price = mini_price
        self.expected_price = expected_price
        self.p_group = p_group
        self.product_type = product_type
        self.items_id = items_id
        
        
    @classmethod
    def get_instance(cls,cursor,items_id): 
    
        items = cursor.execute('''SELECT * FROM items
                                     WHERE items_id = @items_id
                                   ''',{'items_id':items_id})
        items = items.fetchone()
        if items:
            items = cls(*items)
        else:
            items = None
        return items
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS items(
                        product_id INTEGER(20),top_id INTEGER(20),
                        suit_id INTEGER(20),foot_wear_id INTEGER(20),
                        size_id INTEGER(20),qty INTEGER(20),
                        unit_price REAL,total_price REAL,
                        mini_price REAL,expected_price REAL,
                        product_type VARCHAR(50),
                        p_group VARCHAR(35),
                        items_id INTEGER(20),
                        
                        FOREIGN KEY (product_id) REFERENCES product(product_id),
                        FOREIGN KEY (suit_id) REFERENCES suit(suit_id)
                        FOREIGN KEY (top_id) REFERENCES top(top_id)
                        FOREIGN KEY (foot_wear_id) REFERENCES foot_wear(foot_wear_id)
                        FOREIGN KEY (size_id) REFERENCES size(size_id) 
                        )
                       ''')
        
    def add_instance(self,con,sales_id,type_):
        cursor = con.cursor()
        items = self.get_instance(cursor,self.items_id)
        if not items:
            cursor.execute('''INSERT INTO items 
                          VALUES(
                            @product_id,@top_id,@suit_id,
                            @foot_wear_id,@size_id,@qty,
                            @unit_price,@total_price,
                            @mini_price,@expected_price,
                            @p_group,@product_type,@items_id
                            )''',self.__dict__)
            
            if type_ == 'credit':
                cursor.execute('''INSERT INTO credit_sales_iteams 
                                VALUES(
                                    @sales_id,@items_id
                                )
                            ''',{'sales_id':sales_id,'items_id':self.items_id})
            else:
                cursor.execute('''INSERT INTO sales_iteams 
                                VALUES(
                                    @sales_id,@items_id
                                )
                            ''',{'sales_id':sales_id,'items_id':self.items_id})
        con.commit()
      
    @staticmethod  
    def get_items(cursor,type_,id):
        if type_ == 'credit':
            target = 'credit_sales_id'
            table = 'credit_sales_iteams'
        else:
            target = 'sales_id'
            table = 'sales_iteams'
        results = cursor.execute(f''' SELECT * FROM items
                                      JOIN {table} as sale
                                      ON sale.items_id = items.items_id 
                                      WHERE sale.{target} = @id''',{'id':id})
        return results.fetchall()
    
    
    def __str__(self):
        return f"{self.product_type} -- {self.total_price}"
    
    
class Sales:
    def __init__(self, 
                
                 customer_id:int,total_amount:float,
                 logistics:float,expected_price:float,
                 destination:str,remark:str,
                 channel:str,payment_method:str,
                 date:str,purchase_id:str,
                 paid:bool,branch:int,
                 sales_id:int = 0
                 ):
       
        self.customer_id = customer_id
        self.total_amount = total_amount
        self.logistics = logistics
        self.expected_price = expected_price
        self.destination = destination
        self.remark = remark
        self.channel = channel
        self.payment_method = payment_method
        self.date = date
        self.purchase_id = purchase_id
        self.paid= paid
        self.branch = branch 
        self.sales_id = sales_id
        
        
    @classmethod
    def get_instance(cls,cursor,sales_id): 
    
        sales = cursor.execute('''SELECT * FROM sales
                                     WHERE sales_id = @sales_id
                                   ''',{'sales_id':sales_id})
        sales = sales.fetchone()
        if sales:
            sales = cls(*sales)
        else:
            sales = None
        return sales
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
                        customer_id INTEGER(20),
                        total_amount REAL,logistics REAL,
                        expected_price REAL,
                        destination VARCHAR(150),remark VARCHAR(250),
                        channel VARCHAR(10),payment_method VARCHAR(10),
                        date VARCHAR(15),purchase_id VARCHAR(25),
                        paid VARCHAR(5),branch INTEGER(20),
                        sales_id INTEGER(20),
                        
                        FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
                        )
                       ''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales_iteams(
                        sales_id INTEGER(20),items_id INTEGER(20),
                       FOREIGN KEY (sales_id) REFERENCES sales(sales_id),
                       FOREIGN KEY (items_id) REFERENCES items(items_id)
                       )
                       ''')
        
    def add_instance(self,con):
        cursor = con.cursor()
        sales = self.get_instance(cursor,self.sales_id)
        if not sales:
            cursor.execute('''INSERT INTO sales 
                          VALUES(
                            @customer_id,
                            @total_amount,@logistics,
                            @expected_price,
                            @destination,@remark,
                            @channel,@payment_method,
                            @date,@purchase_id,
                            @paid,@branch,
                            @sales_id
                            )''',self.__dict__)
        con.commit()
        
    @staticmethod
    def get_summary(cursor):
        results = cursor.execute('''
                                    SELECT Trim(REPLACE(date,substr(date,-6),'') ) AS date,
                                    payment_method,
                                    sum(total_amount) as total_amount
                                    FROM sales
                                    GROUP BY payment_method,
                                    Trim(REPLACE(date,substr(date,-6),'') )
                                 ''' )
        return results.fetchall()
    
    @staticmethod
    def get_sales(cursor):
        results = cursor.execute('''
                                    SELECT * from sales
                                 ''' )
        
        return results.fetchall()
    
    
    def __str__(self):
        return f"{self.total_amount} -- {self.payment_method}"


