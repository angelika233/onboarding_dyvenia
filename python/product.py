class Product():
    def __init__(self, name, description, seller, reviews, price, available):
        self.name =name
        self.description = description
        self.seller = seller
        self.reviews = set()
        self.price = price
        self.available = available

    def __str__(self):
        return f"Product(name = {self.name}, description = {self.description}, seller = {self.seller}, reviews = {self.reviews}, price = {self.price}, available = {self.available})"