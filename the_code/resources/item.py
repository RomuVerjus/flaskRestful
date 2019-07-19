from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from the_code.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument(
        'name',
        type=str,
        required=False
    )

    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        item = ItemModel(data['name'], data['price'], data['store_id'])

        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': "An item with name '{}' does not exist.".format(name)}, 400

        item.delete()

        return {"message": " Item deleted"}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            item.name = data['name']
            item.store_id = data['store_id']
        else:
            item = ItemModel(data['name'], data['price'], data['store_id'])

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
