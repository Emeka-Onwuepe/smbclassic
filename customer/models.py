class Customer:
    def __init__(self, name:str,phone_number:str, 
                 email:str =None, address:str=None,
                 total_credit:float=0.00,
                 total_payment:float=0.00,
                 balance:float=0.00,
                 customer_id:int = 0
                 ):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.total_credit = total_credit
        self.total_payment = total_payment
        self.balance = balance 
        self.customer_id = customer_id


    def set_id(self,cursor):
        id = cursor.execute('''Select max(customer_id)
                                from customer
                            ''')
        [id] = id.fetchone()
        self.customer_id = id + 2
        
    @classmethod
    def get_instance(cls,cursor,phone_number): 
    
        customer = cursor.execute('''SELECT * FROM customer
                                     WHERE phone_number = @phone_number
                                   ''',{'phone_number':phone_number})
        customer = customer.fetchone()
        if customer:
            customer = cls(*customer)
        else:
            customer = None
        return customer
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS customer(
                       name VARCHAR(100),phone_number VARCHAR(20) UNIQUE,
                       email VARCHAR(35),address VARCHAR(120), 
                       total_credit REAL,total_payment REAL,balance REAL,
                       customer_id INTEGER(20))
                       ''')
        
    def add_instance(self,con,update=False):
        cursor = con.cursor()
        customer = self.get_instance(cursor,self.phone_number)
        
        if not customer:
            if self.customer_id == 0:
                self.set_id(cursor)
            cursor.execute('''INSERT INTO customer 
                          VALUES(@name,@phone_number,@email,@address,
                           @total_credit,@total_payment,@balance,@customer_id)''',self.__dict__)
        elif update:
            self.customer_id = customer.customer_id
            cursor.execute('''UPDATE customer 
                            SET name = @name, phone_number = @phone_number,email =@email,
                            address = @address, total_credit = @total_credit,
                            total_payment = @total_payment,balance = @balance,
                            customer_id = @customer_id
                            WHERE phone_number = @phone_number''',self.__dict__)
            
        else:
            return customer
        if update or not customer:
            con.commit()
        return False
    
    
    def __str__(self):
        return f"{self.name} -- {self.phone_number}"


