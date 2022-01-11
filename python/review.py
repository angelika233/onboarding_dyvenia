class Review ():
    def __init__(self, description, user, product):
        self.description = description
        self.user = user
        self.product = product

    def __str__(self):
        return f"Review(description = {self.description}, user = {self.user}, product = {self.user})"
