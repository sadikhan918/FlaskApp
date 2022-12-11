from my_app.catalog.__init__ import db
from my_app.catalog.models import Waiter, CustomerTicket, Menu

newWaiter = Waiter("John", "Doe", "21", "Y")
db.session.add(newWaiter)
db.session.commit()
