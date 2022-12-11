from my_app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('products', lazy='dynamic'))
        
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category    
    def __repr__(self):
        return '<Product %d>' % self.id

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    #products = db.relationship('Product', backref=db.backref('category'))
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<Category &d>' % self.id    
    
class Waiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    tax_number = db.Column(db.String)
    available = db.Column(db.String)

    def __init__(self, first_name, last_name, tax_number, available):
        self.first_name = first_name
        self.last_name = last_name
        self.tax_number = tax_number
        self.available = available

    def __repr__(self):
            return '<Waiter %d>' % self.id

class CustomerTicket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    arrival = db.Column(db.String)
    departed = db.Column(db.String)
    currentWaiter = db.Column(db.String)

    def __init__(self, arrival, departed, currentWaiter):
        self.arrival = arrival
        self.departed = departed
        self.currentWaiter = currentWaiter

        def __repr__(self):
            return '<CustomerTicket %d>' % self.id


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Numeric)

    def __init__(self, item_name, description, price):
        self.item_name = item_name
        self.description = description
        self.price = price

    def __repr__(self):
            return '<Menu %d>' % self.id

class customerItemsWanted(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ticketId = db.Column(db.Integer)
    itemsWanted = db.Column(db.String)

    def __init__(self, ticketId, itemsWanted):
        self.ticketId = ticketId
        self.itemsWanted = itemsWanted
    
    def __repr__(self):
            return '<customerItemsWanted %d>' % self.id
    
    
