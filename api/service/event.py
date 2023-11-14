from flask_restx import Namespace, Resource, fields
from ..model.inventorymodel import Inventory
from ..utils import db
from flask import request
from http import HTTPStatus

event_namespace = Namespace(
    'events', description='Perform action on inventories')

invent_model = event_namespace.model('InventScheme', {
    'id': fields.Integer(),
    'productName': fields.String(required=True, description='Product name'),
    'price': fields.String(required=True, description='Product price'),
    'quantity': fields.String(required=True, description='Product quantity'),
})
update_model = event_namespace.model('InventUpdateScheme', {
    'productName': fields.String(required=True, description='Product name'),
    'price': fields.String(required=True, description='Product price'),
    'quantity': fields.String(required=True, description='Product quantity'),
})

# endpoints


@event_namespace.route('/create_new_inventories')
class CREATEINVENTORIES(Resource):
    @event_namespace.expect(invent_model)
    @event_namespace.marshal_with(invent_model)
    def post(self):
        '''
            Create new inventories
        '''
        data = request.get_json()
        productName = data['productName']
        price = data['price']
        quantity = data['quantity']

        product_exist = Inventory.query.filter_by(
            productName=productName).first()

        if product_exist:
            response = {
                'message': 'Product exist. Try inputting another product'
            }

            return response, HTTPStatus.UNAUTHORIZED

        else:
            new_inventory = Inventory(
                productName=productName, price=price, quantity=quantity)
            new_inventory.save()

            return new_inventory, HTTPStatus.CREATED

# Retrieve information based on Items Stock Keeping Unit (id)


@event_namespace.route('/retrieve/product/<int:id>')
class RETRIEVEITEMS(Resource):
    @event_namespace.marshal_with(invent_model)
    def get(self, id):
        '''
            Get Items based on the product unique integer
        '''
        product = Inventory.query.filter_by(id=id).first()
        return product, HTTPStatus.OK

# Retrieve all items


@event_namespace.route('/retrieve/all_items')
class RETRIEVEALLITEMS(Resource):
    @event_namespace.marshal_with(invent_model)
    def get(self):
        '''
            Get all items
        '''
        all_products = Inventory.query.all()
        return all_products, HTTPStatus.OK

# Modify|Update existing items e.g quantity, price


@event_namespace.route('/update/product/<int:id>')
class MODIFYITEMS(Resource):
    @event_namespace.expect(update_model)
    @event_namespace.marshal_with(invent_model)
    def put(self, id):
        '''
            Update existing items
        '''
        data = request.get_json()
        product = Inventory.query.filter_by(id=id).first()
        product.productName = data['productName']
        product.price = data['price']
        product.quantity = data['quantity']

        db.session.commit()
        return product, HTTPStatus.CREATED


# Delete items from inventory
@event_namespace.route('/delete/product/<int:id>')
class DELETE_ITEMS_FROM_INVENTORY(Resource):
    def delete(self, id):
        '''
            Delete items from the inventory
        '''
        product = Inventory.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()

        response = {
            "message": f'Deleted product id of -{id} successfully'
        }

        return response, HTTPStatus.MOVED_PERMANENTLY
