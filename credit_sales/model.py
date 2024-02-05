from datetime import datetime


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
        self.p_total_amount = total_amount
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
            credit_sales = credit_sales[:2] + credit_sales[3:]
            credit_sales = cls(*credit_sales)
        else:
            credit_sales = None
        return credit_sales
    
    @classmethod
    def get_customer_credits(cls,cursor,phone_number): 
    
        credit_sales = cursor.execute('''SELECT * FROM credit_sales
                                        WHERE customer_id = (SELECT customer_id 
                                                            FROM customer
                                                            WHERE phone_number = @phone_number
                                                            ) and balance < 0
                                   ''',{'phone_number':phone_number})
        credit_sales = credit_sales.fetchall()
        credit_sales_ = []
        if credit_sales:
            for credit_sale in credit_sales:
                credit_sale = credit_sale[:2] + credit_sale[3:]
                credit_sale = cls(*credit_sale)
                credit_sales_.append(credit_sale)
        return credit_sales_
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS credit_sales(
                        customer_id INTEGER(20),
                        total_amount REAL,p_total_amount REAL,
                        total_payment REAL,
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
                            @total_amount,
                            @p_total_amount,
                            @total_payment,
                            @balance,@expected_price,
                            @remark,
                            @channel,@payment_method,
                            @date,@purchase_id,
                            @fully_paid,@branch,
                            @credit_sales_id
                            )''',self.__dict__)
        con.commit()
    
    @staticmethod
    def update_instance(con,amount,purchase_id):
        cursor = con.cursor()
        
        cursor.execute('''UPDATE credit_sales 
                          SET total_payment = total_payment + @amount,
                          balance = balance + @amount
                          WHERE purchase_id = purchase_id
                          ''',{'amount':amount,'purchase_id':purchase_id})
        con.commit()
        
    @staticmethod
    def get_summary(cursor):
        date =  datetime.now().strftime("%d/%b/%Y")
        results = cursor.execute('''
                                 SELECT customer.name,customer.phone_number,
                                 sum(total_amount) as total,
                                 Trim(REPLACE(date,substr(date,-6),'') ) as date
                                 FROM credit_sales
                                 JOIN customer
                                 ON customer.customer_id = credit_sales.customer_id
                                 WHERE Trim(REPLACE(date,substr(date,-6),'') ) = @date
                                 GROUP BY customer.customer_id,
                                 Trim(REPLACE(date,substr(date,-6),'') )
                                 ''',{'date':date} )
        return results.fetchall()
        
        
    @staticmethod
    def get_credit_sales(cursor,ids):
        string = ''
        # ids = string.join(ids)
        # print(ids)
        index = 0
        last = len(ids) - 1
        for id in ids:
            if index < last:
                string+=f'?,'
            else:
                string+=f'?'
            index += 1
        
        querry =f'''SELECT credit_sales.*,
                    c.phone_number,c.email,
                    c.name,c.address
                    from credit_sales
                    JOIN customer as c
                    ON c.customer_id = credit_sales.customer_id
                    where credit_sales_id in ({string})
                                 '''
        results = cursor.execute(querry, ids)
        
        return results.fetchall()
    
    @staticmethod
    def delete_credit_sale(con,credit_sales_id):
        cursor = con.cursor()
        cursor.execute('''DELETE FROM  items
                          WHERE items_id = (SELECT items_id
                                            FROM credit_sales_iteams
                                            WHERE credit_sales_id = @credit_sales_id)
                            ''',{'credit_sales_id':credit_sales_id})
        cursor.execute('''DELETE FROM  credit_sales_iteams
                          WHERE credit_sales_id = @credit_sales_id
                            ''',{'credit_sales_id':credit_sales_id})
        con.commit()
    
    def __str__(self):
        return f"{self.total_amount} -- {self.payment_method}"
    
    
class Payment:
    def __init__(self, 
                 credit_sales_id:int, amount:float,
                 date:str,purchase_id:str
                 ):
       
        self.credit_sales_id = credit_sales_id
        self.amount = amount
        self.date = date
        self.purchase_id = purchase_id
        self.id = 0
    
        
        
    @classmethod
    def get_instance(cls,cursor,target,customer=False): 
        
        if customer:
            payment = cursor.execute('''SELECT rowid,* FROM payment
                                     WHERE credit_sales_id in ( select credit_sales_id
                                                                from credit_sales
                                                                where customer_id = (select customer_id 
                                                                                    from customer
                                                                                    where phone_number = @phone_number )
                                                                )
                                   ''',{'phone_number':target})
        else:    
             payment = cursor.execute('''SELECT * FROM payment
                                     WHERE purchase_id = @purchase_id
                                   ''',{'purchase_id':target})
        
        payments = payment.fetchall()
        payment_ = []
        if payments:
            for payment in payments:
                if customer:
                    id = payment[0]
                    rest = payment[1:]
                    payment = cls(*rest)
                    payment.id = id
                else:
                   payment = cls(*payment) 
                payment_.append(payment)
        return payment_
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS payment(
                        credit_sales_id INTEGER(20),
                        amount REAL,date VARCHAR(15),
                        purchase_id INTEGER(20),
                        
                        FOREIGN KEY (credit_sales_id) REFERENCES credit_sales(credit_sales_id)
                        )
                       ''')
        
        
    def add_instance(self,con):
        cursor = con.cursor()
        # payment = self.get_instance(cursor,self.purchase_id)
        # if not payment:
        cursor.execute('''INSERT INTO payment 
                          VALUES(
                            @credit_sales_id,
                            @amount,@date,
                            @purchase_id
                            )''',self.__dict__)
        con.commit()
        
    @staticmethod  
    def update_instance(con,amount,rowid):
        cursor = con.cursor()
        cursor.execute('''UPDATE payment 
                          SET amount = @amount
                          WHERE rowid = @rowid
                            ''',{'amount':amount,'rowid':rowid})
        con.commit()
    
    @staticmethod  
    def delete_instance(con,rowid):
        cursor = con.cursor()
        cursor.execute('''DELETE FROM payment 
                          WHERE rowid = @rowid
                            ''',{'rowid':rowid})
        con.commit()
        
    @staticmethod
    def get_summary(cursor):
        results = cursor.execute('''
                                    SELECT customer.name,customer.phone_number,
                                    sum(payment.amount) as amount,
                                    Trim(REPLACE(payment.date,substr(payment.date,-6),'') ) as date
                                    from payment
                                    JOIN credit_sales
                                    ON payment.credit_sales_id = credit_sales.credit_sales_id
                                    JOIN customer
                                    ON customer.customer_id = credit_sales.customer_id
                                    GROUP BY customer.customer_id,
                                    Trim(REPLACE(payment.date,substr(payment.date,-6),'') )
                                 ''' )
        return results.fetchall()
    
    @staticmethod
    def get_payments(cursor):
        results = cursor.execute('''SELECT rowid,* FROM payment''')
        return results.fetchall()
    
    def __str__(self):
        return f"{self.date} -- {self.amount}"

