class Credit_Sales:
    def __init__(self, 
                 customer_id:int,total_amount:float,
                 total_payment:float,balance:float,
                 expected_price:float,remark:str,
                 channel:str,payment_method:str,
                 date:str,purchase_id:str,
                 fully_paid:bool,branch:int,
                 credit_sales_id:int = 0
                 ):
       
        self.customer_id = customer_id
        self.total_amount = total_amount
        self.total_payment = total_payment
        self.balance = balance
        self.expected_price = expected_price
        self.remark = remark
        self.channel = channel
        self.payment_method = payment_method
        self.date = date
        self.purchase_id = purchase_id
        self.fully_paid= fully_paid
        self.branch = branch 
        self.credit_sales_id = credit_sales_id
        
        
    @classmethod
    def get_instance(cls,cursor,credit_sales_id): 
    
        credit_sales = cursor.execute('''SELECT * FROM credit_sales
                                     WHERE credit_sales_id = @credit_sales_id
                                   ''',{'credit_sales_id':credit_sales_id})
        credit_sales = credit_sales.fetchone()
        if credit_sales:
            credit_sales = cls(*credit_sales)
        else:
            credit_sales = None
        return credit_sales
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS credit_sales(
                        customer_id INTEGER(20),
                        total_amount REAL,total_payment REAL,
                        balance REAL,expected_price REAL,
                        remark VARCHAR(250),
                        channel VARCHAR(10),payment_method VARCHAR(10),
                        date VARCHAR(15),purchase_id VARCHAR(25),
                        fully_paid VARCHAR(5),branch INTEGER(20),
                        credit_sales_id INTEGER(20),
                        
                        FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
                        )
                       ''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS credit_sales_iteams(
                        credit_sales_id INTEGER(20),items_id INTEGER(20),
                       FOREIGN KEY (credit_sales_id) REFERENCES credit_sales(credit_sales_id),
                       FOREIGN KEY (items_id) REFERENCES items(items_id)
                       )
                       ''')
        
    def add_instance(self,con):
        cursor = con.cursor()
        credit_sales = self.get_instance(cursor,self.credit_sales_id)
        if not credit_sales:
            cursor.execute('''INSERT INTO credit_sales 
                          VALUES(
                            @customer_id,
                            @total_amount,@total_payment,
                            @balance,@expected_price,
                            @remark,
                            @channel,@payment_method,
                            @date,@purchase_id,
                            @fully_paid,@branch,
                            @credit_sales_id
                            )''',self.__dict__)
        con.commit()
    
    
    def __str__(self):
        return f"{self.total_amount} -- {self.payment_method}"
    
    
class Payment:
    def __init__(self, 
                
                 credit_sales_id:int, amount:float,
                 date:str, payment_id:int = 0
                 ):
       
        self.credit_sales_id = credit_sales_id
        self.amount = amount
        self.date = date
        self.payment_id = payment_id
        
        
    @classmethod
    def get_instance(cls,cursor,payment_id): 
    
        credit_sales = cursor.execute('''SELECT * FROM credit_sales
                                     WHERE payment_id = @payment_id
                                   ''',{'payment_id':payment_id})
        credit_sales = credit_sales.fetchone()
        if credit_sales:
            credit_sales = cls(*credit_sales)
        else:
            credit_sales = None
        return credit_sales
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS credit_sales(
                        credit_sales_id INTEGER(20),
                        amount REAL,date VARCHAR(15),
                        payment_id INTEGER(20),
                        
                        FOREIGN KEY (credit_sales_id) REFERENCES credit_sales(credit_sales_id)
                        )
                       ''')
        
        
    def add_instance(self,con):
        cursor = con.cursor()
        credit_sales = self.get_instance(cursor,self.payment_id)
        if not credit_sales:
            cursor.execute('''INSERT INTO credit_sales 
                          VALUES(
                            @credit_sales_id,
                            @amount,@date,
                            @payment_id,
                            )''',self.__dict__)
        con.commit()
    
    
    def __str__(self):
        return f"{self.date} -- {self.amount}"

