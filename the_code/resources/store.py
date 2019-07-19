from flask_restful import Resource, reqparse

from the_code.models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='The store\'s name is required'
    )

    @classmethod
    def get(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store not found."}, 404

    def post(self, name):
        data = Store.parser.parse_args()

        if StoreModel.find_by_name(name):
            return {"message": "The store already exists."}

        store = StoreModel(data['name'])

        store.save_to_db()

        return {"message": "The store has been created."}

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "The store is deleted."}, 200

        return {"message": "The store does not exist."}, 400


class StoreList(Resource):
    def list(self):
        return StoreModel.query.all()
