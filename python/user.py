from product import Product


class User():
    from product import Product
    from review import Review
    def __init__(self, id, name):
        self.name =name
        self.id = id
        self.reviews = set()

    def __str__(self):
        return f"User(id = {self.id}, name = {self.name})"
    
    def sell_product(self, name, description, price):
        return Product(name, description, self.name, set(),  price, available=True)

    def buy_product(type, object):
        if object.available == True:
            object.available = False
        else:
            print("This product is unavailable")
            

    def write_review(self,description, object):
        rev = self.Review(description, self.name, object.name)
        object.reviews.add(rev)
        self.reviews.add(rev)
        return rev
