import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Product, Order

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Produce': Product, 'Order': Order}