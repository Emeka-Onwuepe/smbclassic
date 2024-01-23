# Product_Abstract
class Querried_Product_Class:
    suits = []
    def __init__(self, type:str,
                 brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str
                 ):
        self.type = type
        self.brand = brand
        # self.description = description
        self.color = color
        self.gender = gender
        self.age_group = age_group
        
                      

class Querried_Product(Querried_Product_Class):    
    def __init__(self,type:str,brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str,
                 product_type_id:int,
                 product_id:int,
                 product_type:str,
                 size_id:int,
                 category:str,
                 price:float,
                 size: str,
                 pgroup:str,
                 ):
        
        super().__init__(type,brand,description,
                          color,gender,age_group
                          ) 
        # self.product_type_id = product_type_id
        # self.product_id = product_id
        self.product_type = product_type
        # self.size_id = size_id
        self.category = category
        self.price = price
        self.size = size
        self.pgroup = pgroup
        self.id = f'{product_id}-{size_id}'
        
    def __str__(self) -> str:
        return f'{self.product_type}-{self.category}-{self.size} -{self.price}'
        
        
class Querried_Suit(Querried_Product_Class):    
    def __init__(self,type:str,brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str,
                 product_type_id:int,
                 breasted:str,
                 button:str,
                 pics:str,
                 golden_button:str,
                 suit_id:int,
                 product_type:str,
                 size_id:int,
                 category:str,
                 price:float,
                 size: str,
                 pgroup:str
                 
                 ):
        
        super().__init__(type,brand,description,
                          color,gender,age_group
                          ) 
        # self.product_type_id = product_type_id
        self.breasted = breasted
        self.button = button
        self.pics = pics
        self.golden_button = golden_button
        # self.suit_id = suit_id
        self.product_type = product_type
        # self.size_id = size_id
        self.category = category
        self.price = price
        self.size = size
        self.pgroup = pgroup
        self.id = f'{suit_id}-{size_id}'
        
    def __str__(self) -> str:
        return f'{self.product_type}-{self.category}-{self.size} -{self.price}'
          
    
   
class Querried_Top(Querried_Product_Class):    
    def __init__(self,type:str,brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str,
                 product_type_id:int,
                 sleeves:str,
                 top_id:int,
                 product_type:str,
                 size_id:int,
                 category:str,
                 price:float,
                 size: str,
                 pgroup:str
                 ):
        
        super().__init__(type,brand,description,
                          color,gender,age_group
                          ) 
        # self.product_type_id = product_type_id
        self.sleeves = sleeves
        # self.top_id = top_id
        self.product_type = product_type
        # self.size_id = size_id
        self.category = category
        self.price = price
        self.size = size
        self.pgroup = pgroup
        self.id = f'{top_id}-{size_id}'
        
    def __str__(self) -> str:
        return f'{self.product_type}-{self.size} -{self.price}'

class Querried_Foot_Wear(Querried_Product_Class):    
    def __init__(self,type:str,brand:str,
                 description:str,
                 color:str,gender:str,
                 age_group:str,
                 product_type_id:int,
                 sole_color:str,
                 foot_wear_id:int,
                 product_type:str,
                 size_id:int,
                 category:str,
                 price:float,
                 size: str,
                 pgroup:str
                 ):
        
        super().__init__(type,brand,description,
                          color,gender,age_group
                          ) 
        # self.product_type_id = product_type_id
        self.sole_color = sole_color
        # self.foot_wear_id = foot_wear_id
        self.product_type = product_type
        # self.size_id = size_id
        self.category = category
        self.price = price
        self.size = size
        self.pgroup = pgroup
        self.id = f'{foot_wear_id}-{size_id}'
        
    def __str__(self) -> str:
        return f'{self.product_type}-{self.size} -{self.price}'