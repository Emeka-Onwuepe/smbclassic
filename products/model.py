class Category:
    def __init__(self, name:str,
                 category_id:int = 0
                 ):
        self.name = name 
        self.category_id = category_id
         
    @classmethod
    def get_instance(cls,cursor,name): 
    
        category = cursor.execute('''SELECT * FROM category
                                     WHERE name = @name
                                   ''',{'name':name})
        category = category.fetchone()
        if category:
            category = cls(*category)
        else:
            category = None
        return category
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS category(
                       name VARCHAR(100), category_id INTEGER(20))
                       ''')
        
    def add_instance(self,con):
        cursor = con.cursor()
        category = self.get_instance(cursor,self.name)
        if not category:
            cursor.execute('''INSERT INTO category 
                          VALUES(@name,@category_id)''',self.__dict__)
        con.commit()
    
    
    def __str__(self):
        return self.name

# Product_Type
class Product_Type:
    def __init__(self, name:str,
                 category_id:int,
                 p_group:str,
                 product_type_id:int = 0,
                 ):
        self.name = name 
        self.category_id = category_id
        self.p_group = p_group
        self.product_type_id = product_type_id
         
    @classmethod
    def get_instance(cls,cursor,name): 
    
        product_type = cursor.execute('''SELECT * FROM product_type
                                     WHERE name = @name
                                   ''',{'name':name})
        product_type = product_type.fetchone()
        if product_type:
            product_type = cls(*product_type)
        else:
            product_type = None
        return product_type
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS product_type(
                       name VARCHAR(100),category_id INTEGER(20),
                       p_group VARCHAR(15), product_type_id INTEGER(20),
                       FOREIGN KEY (category_id) REFERENCES category(category_id)
                       )
                       ''')
        
    def add_instance(self,con):
        cursor = con.cursor()
        product_type = self.get_instance(cursor,self.name)
        if not product_type:
            cursor.execute('''INSERT INTO product_type 
                          VALUES(@name,@category_id,@p_group,@product_type_id)''',self.__dict__)
        con.commit()
    
    
    def __str__(self):
        return f'{self.name} -- {self.p_group}'
    
# Size
class Size:
    def __init__(self, size:str,
                 product_type_id:int,
                 age_group:str,
                 gender:str,
                 price:float=0.0,
                 size_id:int = 0
                 ):
        self.size = size 
        self.product_type_id = product_type_id
        self.age_group = age_group
        self.gender = gender
        self.price = price
        self.size_id = size_id
         
    @classmethod
    def get_instance(cls,cursor,size_id): 
    
        size = cursor.execute('''SELECT * FROM size
                                     WHERE size_id = @size_id
                                   ''',{'size_id':size_id})
        size = size.fetchone()
        if size:
            size = cls(*size)
        else:
            size = None
        return size
    
    @staticmethod
    def create_table(cursor):
        cursor.execute('''CREATE TABLE IF NOT EXISTS size(
                       size VARCHAR(10),product_type_id INTEGER(20),
                       age_group VARCHAR(10),gender VARCHAR(10), 
                       price REAL,size_id INTEGER(20),
                       
                       FOREIGN KEY (product_type_id) REFERENCES product_type(product_type_id)
                       )
                       ''')
        
    def add_instance(self,con):
        cursor = con.cursor()
        size = self.get_instance(cursor,self.size)
        if not size:
            cursor.execute('''INSERT INTO size 
                          VALUES(@size,@product_type_id,@age_group,
                          @gender,@price,@size_id)''',self.__dict__)
        con.commit()
    
    
    def __str__(self):
        return f'{self.size} -- {self.age_group}'
    
# Product_Abstract
class Product_Class:
    def __init__(self, type:str,
                 brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str
                 ):
        self.type = type
        self.brand = brand
        self.description = description
        self.color = color
        self.gender = gender
        self.age_group = age_group
        
    int_str = ('type VARCHAR(50), brand VARCHAR(50),'
                'description VARCHAR(150), color VARCHAR(50),'
                'gender VARCHAR(10),age_group VARCHAR(10), ')
    
    add_str = ('@type,@brand,@description,@color,@gender,@age_group, ')
                      

class Product(Product_Class):    
    def __init__(self,type:str,brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str,
                 product_type_id:int,
                 product_id:int =0
                 ):
        
        super().__init__(type,brand,description,
                          color,gender,age_group
                          ) 
        self.product_type_id = product_type_id
        self.product_id = product_id
        
    @classmethod
    def get_instance(cls,cursor,product_id): 
    
        product = cursor.execute('''SELECT * FROM product
                                     WHERE product_id = @product_id
                                   ''',{'product_id':product_id})
        product = product.fetchone()
        if product:
            product = cls(*product)
        else:
            product = None
        return product   
   
    @staticmethod
    def create_table(cursor):
        querry =  f'''
                    CREATE TABLE IF NOT EXISTS product({Product_Class.int_str}
                    product_type_id INTEGER(20),product_id INTEGER(20), 
                     FOREIGN KEY (product_type_id) REFERENCES product_type(product_type_id)
                       )
                  '''
        cursor.execute(querry)
        cursor.execute('''CREATE TABLE IF NOT EXISTS product_sizes(
                        product_id INTEGER(20),size_id INTEGER(20),
       
                       FOREIGN KEY (product_id) REFERENCES product(product_id)
                       FOREIGN KEY (size_id) REFERENCES size(size_id)
                       )
                       ''')
    
    def add_instance(self,con):
        cursor = con.cursor()
        size = self.get_instance(cursor,self.size)
        if not size:
            cursor.execute(f'''INSERT INTO size 
                          VALUES({Product_Class.add_str}
                              @product_type_id,@product_id)''',self.__dict__)
        con.commit()
        
    def add_m2m(self,con,size_id):
        cursor = con.cursor()
        m2m = cursor.execute('''SELECT * FROM product_sizes
                                     WHERE product_id = @product_id
                                     and size_id = @size_id
                                   ''',{'product_id':self.product_id,
                                        'size_id':size_id})
        m2m = m2m.fetchone()
        if not m2m:
            cursor.execute(f'''INSERT INTO product_sizes 
                          VALUES(@product_id,@size_id)''',{'product_id':self.product_id,
                                        'size_id':size_id})
        con.commit()        
    
        
        
class Suit(Product_Class):    
    def __init__(self,type:str,brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str,
                 product_type_id:int,
                 breasted:str,
                 button:str,
                 pics:str,
                 golden_button:str,
                 suit_id:int =0
                 ):
        
        super().__init__(type,brand,description,
                          color,gender,age_group
                          ) 
        self.product_type_id = product_type_id
        self.breasted = breasted
        self.button = button
        self.pics = pics
        self.golden_button = golden_button
        self.suit_id = suit_id
        
    @classmethod
    def get_instance(cls,cursor,suit_id): 
    
        suit = cursor.execute('''SELECT * FROM suit
                                     WHERE suit_id = @suit_id
                                   ''',{'suit_id':suit_id})
        suit = suit.fetchone()
        if suit:
            suit = cls(*suit)
        else:
            suit = None
        return suit   
   
    @staticmethod
    def create_table(cursor):
    
        querry =  f'''
                    CREATE TABLE IF NOT EXISTS suit({Product_Class.int_str}
                    product_type_id INTEGER(20),breasted VARCHAR(15),
                    button VARCHAR(15),pics VARCHAR(3),golden_button VARCHAR(30),
                    suit_id INTEGER(20), 
                    FOREIGN KEY (product_type_id) REFERENCES product_type(product_type_id)
                       )
                  '''
        cursor.execute(querry)
        cursor.execute('''CREATE TABLE IF NOT EXISTS suit_sizes(
                        suit_id INTEGER(20),size_id INTEGER(20),
                       FOREIGN KEY (suit_id) REFERENCES suit(suit_id)
                       FOREIGN KEY (size_id) REFERENCES size(size_id)
                       )
                       ''')
    
    def add_instance(self,con):
        cursor = con.cursor()
        size = self.get_instance(cursor,self.suit_id)
        if not size:
            cursor.execute(f'''INSERT INTO suit 
                          VALUES({Product_Class.add_str}
                              @product_type_id,
                              @breasted,@button,@pics,
                              @golden_button,
                              @suit_id)''',self.__dict__)
        con.commit() 
    
    def add_m2m(self,con,size_id):
        cursor = con.cursor()
        m2m = cursor.execute('''SELECT * FROM suit_sizes
                                     WHERE suit_id = @suit_id
                                     and size_id = @size_id
                                   ''',{'suit_id':self.suit_id,
                                        'size_id':size_id})
        m2m = m2m.fetchone()
        if not m2m:
            cursor.execute(f'''INSERT INTO suit_sizes 
                          VALUES(@suit_id,@size_id)''',{'suit_id':self.suit_id,
                                        'size_id':size_id})
        con.commit()        
    
   
class Top(Product_Class):    
    def __init__(self,type:str,brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str,
                 product_type_id:int,
                 sleeves:str,
                 top_id:int =0
                 ):
        
        super().__init__(type,brand,description,
                          color,gender,age_group
                          ) 
        self.product_type_id = product_type_id
        self.sleeves = sleeves
        self.top_id = top_id
        
    @classmethod
    def get_instance(cls,cursor,top_id): 
    
        top = cursor.execute('''SELECT * FROM top
                                     WHERE top_id = @top_id
                                   ''',{'top_id':top_id})
        top = top.fetchone()
        if top:
            top = cls(*top)
        else:
            top = None
        return top   
   
    @staticmethod
    def create_table(cursor):
    
        querry =  f'''
                    CREATE TABLE IF NOT EXISTS top({Product_Class.int_str}
                    product_type_id INTEGER(20),sleeves VARCHAR(15),
                    top_id INTEGER(20), 
                    FOREIGN KEY (product_type_id) REFERENCES product_type(product_type_id)
                       )
                  '''
        cursor.execute(querry)
        cursor.execute('''CREATE TABLE IF NOT EXISTS top_sizes(
                        top_id INTEGER(20),size_id INTEGER(20),
                       FOREIGN KEY (top_id) REFERENCES top(top_id)
                       FOREIGN KEY (size_id) REFERENCES size(size_id)
                       )
                       ''')
    
    def add_instance(self,con):
        cursor = con.cursor()
        size = self.get_instance(cursor,self.size)
        if not size:
            cursor.execute(f'''INSERT INTO size 
                          VALUES({Product_Class.add_str}
                              @product_type_id,
                              @sleeves,
                              @top_id)''',self.__dict__)
        con.commit()   
        
    def add_m2m(self,con,size_id):
            cursor = con.cursor()
            m2m = cursor.execute('''SELECT * FROM top_sizes
                                        WHERE top_id = @top_id
                                        and size_id = @size_id
                                    ''',{'top_id':self.top_id,
                                            'size_id':size_id})
            m2m = m2m.fetchone()
            if not m2m:
                cursor.execute(f'''INSERT INTO top_sizes 
                            VALUES(@top_id,@size_id)''',{'top_id':self.top_id,
                                                            'size_id':size_id})
            con.commit()       

class Foot_Wear(Product_Class):    
    def __init__(self,type:str,brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str,
                 product_type_id:int,
                 sole_color:str,
                 foot_wear_id:int =0
                 ):
        
        super().__init__(type,brand,description,
                          color,gender,age_group
                          ) 
        self.product_type_id = product_type_id
        self.sole_color = sole_color
        self.foot_wear_id = foot_wear_id
        
    @classmethod
    def get_instance(cls,cursor,foot_wear_id): 
    
        foot_wear = cursor.execute('''SELECT * FROM foot_wear
                                     WHERE foot_wear_id = @foot_wear_id
                                   ''',{'foot_wear_id':foot_wear_id})
        foot_wear = foot_wear.fetchone()
        if foot_wear:
            foot_wear = cls(*foot_wear)
        else:
            foot_wear = None
        return foot_wear   
   
    @staticmethod
    def create_table(cursor):
    
        querry =  f'''
                    CREATE TABLE IF NOT EXISTS foot_wear({Product_Class.int_str}
                    product_type_id INTEGER(20),sole_color VARCHAR(15),
                    foot_wear_id INTEGER(20), 
                    FOREIGN KEY (product_type_id) REFERENCES product_type(product_type_id)
                       )
                  '''
        cursor.execute(querry)
        cursor.execute('''CREATE TABLE IF NOT EXISTS foot_wear_sizes(
                        foot_wear_id INTEGER(20),size_id INTEGER(20),
                       FOREIGN KEY (foot_wear_id) REFERENCES foot_wear(foot_wear_id)
                       FOREIGN KEY (size_id) REFERENCES size(size_id)
                       )
                       ''')
    
    def add_instance(self,con):
        cursor = con.cursor()
        size = self.get_instance(cursor,self.size)
        if not size:
            cursor.execute(f'''INSERT INTO size 
                          VALUES({Product_Class.add_str}
                              @product_type_id,
                              @sole_color,
                              @foot_wear_id)''',self.__dict__)
        con.commit()  
        
    def add_m2m(self,con,size_id):
        cursor = con.cursor()
        m2m = cursor.execute('''SELECT * FROM foot_wear_sizes
                                        WHERE foot_wear_id = @foot_wear_id
                                        and size_id = @size_id
                                    ''',{'foot_wear_id':self.foot_wear_id,
                                            'size_id':size_id})
        m2m = m2m.fetchone()
        if not m2m:
            cursor.execute(f'''INSERT INTO foot_wear_sizes 
                            VALUES(@foot_wear_id,@size_id)''',{'foot_wear_id':self.foot_wear_id,
                                                                'size_id':size_id})
        con.commit()   