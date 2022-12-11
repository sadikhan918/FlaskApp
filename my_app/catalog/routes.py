from flask import request, jsonify, Blueprint
from my_app import db
from my_app.catalog.models import Product, Category, Waiter, Menu, CustomerTicket, customerItemsWanted

catalog = Blueprint('catalog', __name__)

@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."

@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    return 'Product - %s, $%s' % (product.name, product.price)

@catalog.route('/products')
def products():
    products = Product.query.all()
    res = {}
    for product in products:
        res[product.id] = {
            'name': product.name,
            'price': product.price,
            'category': product.category.name
        }
    return jsonify(res)

@catalog.route('/product-create', methods=['POST',])
def creat_product():
    name = request.json.get('name')
    price = request.json.get('price')
    categ_name = request.json.get('category')
    category = Category.query.filter_by(name=categ_name).first()
    if not category:
        category = Category(categ_name)
    product = Product(name, price, category)
    db.session.add(product)
    db.session.commit()
    return 'Product created.'

@catalog.route('/category-create', methods=['POST', ])
def create_category():
    name = request.json.get('name')
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return 'Category created'

@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    res = {}
    for category in categories:
        res[category.id] = {
            'name': category.name
        }
        for product in category.products:
            res[category.id]['products'] = {
                'id': product.id,
                'name': product.name,
                'price': product.price}
    return jsonify(res)

@catalog.route('/waiters')
def getWaiters():
    waiters = Waiter.query.all()
    res = {}
    for waiter in waiters:
        res[waiter.id] = {
            'first_name': waiter.first_name,
            'last_name': waiter.last_name,
            'available': waiter.available
        }
    return jsonify(res)

@catalog.route('/ReturnMenu')
def returnMenu():
    menu = Menu.query.all()
    res = {}
    for item in menu:
        res[menu.id] = {
            'item_name': menu.item_name,
            'description': menu.description,
            'price': menu.price
        }
    return jsonify(res)

@catalog.route('/ReturnCustomerTickets')
def returnCustomerTickets():
    tickets = CustomerTicket.query.all()
    res = {}
    for ticket in tickets:
        res[ticket.id] = {
            'arrival': ticket.arrival,
            'departed': ticket.departed,
            'currentWaiter': ticket.currentWaiter
        }
    return jsonify(res)

@catalog.route('/CreateTicket', methods=['POST', ])
def createTicket():
    arrival = request.json.get('arrival')
    departed = request.json.get('departed')
    available_waiter_id = Waiter.query.filter_by(available = 'Y').first().id
    available_waiter = Waiter.query.filter_by(available = 'Y').first()
    waiter_id_for_ticket = available_waiter_id
    itemsWanted = request.json.get('itemsWanted')
    
    ticket = CustomerTicket(arrival, departed, available_waiter_id)
    db.session.add(ticket)
    db.session.commit()

    orderID = CustomerTicket.query.filter_by(currentWaiter = waiter_id_for_ticket).first().id
    wantedItems = customerItemsWanted(orderID, itemsWanted)
    available_waiter.available = 'N'
    db.session.add(wantedItems)
    db.session.commit()
    
    return 'Ticket Created'

@catalog.route('/RegisterWaiter', methods=['POST', ])
def registerWaiter():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    tax_number = request.json.get('tax_number')
    available = 'Y'

    newWaiter = Waiter(first_name, last_name, tax_number, available)
    db.session.add(newWaiter)
    db.session.commit()
    return 'Waiter Registered'

@catalog.route('/CreateMenu', methods=['POST', ])
def createMenu():
    import json
    data = json.loads(request.data)
    for iterator in data:
        item_name = iterator['item_name']
        description = iterator['description']
        price = iterator['price']
        newItem = Menu(item_name, description, price)
        db.session.add(newItem)
        db.session.commit()
    return 'Menu items added'

@catalog.route('/GetCostOfTicket', methods=['POST', ])
def getItemsWanted():
    customerTicketID = request.json.get('id')
    orderID = str(customerItemsWanted.query.filter_by(ticketId = customerTicketID).first().itemsWanted)
    li = list(orderID.split(" "))
    price = 0
    for item in li:
        matchingFood = Menu.query.filter_by(id = item).first().price
        price += matchingFood
    res = {'price': price}
    return jsonify(res)

@catalog.route('/GetCostOfAllTicket')
def getCostOfAllTickets():
    tickets = CustomerTicket.query.all()
    price = 0
    for ticket in tickets:
        customerTicketId = ticket.id
        if(customerItemsWanted.query.filter_by(ticketId = customerTicketId).first() is not None):
            relatedOrderID = customerItemsWanted.query.filter_by(ticketId = customerTicketId).first().itemsWanted
            relatedOrderIDString = str(relatedOrderID)
            li = list(relatedOrderIDString.split(" "))
            for item in li:
                if(Menu.query.filter_by(id = item).first() is not None):
                    matchingFood = Menu.query.filter_by(id = item).first().price
                    price += matchingFood
    res = {'price': price}
    return jsonify(res)
        

