from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

#create an Item Resource contient get & post methods
class Item(Resource):

    # creating a parser to allow just some element to be passed in 
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
            type=float, 
            required=True, 
            help="this field cannot be left blank")

    """
    parser.add_argument('store_id', 
            type=int, 
            required=True, 
            help="Every item needs a store id")
    """
    @jwt_required()
    def get(self, name): # get item by name
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message" : "item not found"}, 500

    def post(self, name): # post to add an item to the list

        if ItemModel.find_by_name(name):
            return {"message" : "An item with name {} already exist".format(name)}

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price']) # **data == data['price'], data['store_id']

        try:
            Item.insert()
        except:
            return {"message" : "An error occured inserting the item"}, 500

        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            
        return {"message" : "item deleted"}

    def put(self, name):
        data = ItemModel.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            try:
                item.price = data['price']  
            except:
                return {"message" : 'An error accured updating the item the item'}, 500
        else:
            try:
                item = ItemModel(name, data['price'])
            except:
                return {"message" : 'An error accured inserting the item'}, 500
        
        item.save_to_db()

        return item.json()


class Itemlist(Resource):
    def get(self): # get all created items
        return {'items' : [item.json() for item in ItemModel.query.all()] }
       #return {'items' : list(map(lambda x : x.json(), ItemModel.query.all())) }