from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSON

from document import Base, TableNames

from jsonschema import validate, ValidationError

class MenuItem(Base):
    __tablename__ = TableNames.MENU_ITEM.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_item = Column(JSON, nullable=False)

    SCHEMA = {
        'type' : 'array',
        'items' : {
            'type' : 'object',
            'properties' : {
                'name' : {
                    'type' : 'string'
                },
                'item_type' : {
                    'type' : 'string'
                    'enum' : ['appetizer', 'entree', 'dessert', 'drink', 'premade', 'addon']
                },
                'price' : {
                    'type' : 'number'
                },
                'type' : {
                    'type' : 'string'
                }
            }
        }
    }

    @staticmethod
    def factory(json_dict):
        try:
            validate(json_dict, MenuItem.SCHEMA)
            return MenuItem(
                menu_item = json_dict
            )
        except ValidationError:
            return None
                    
