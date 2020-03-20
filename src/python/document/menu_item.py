from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from document import Base, TableNames

from jsonschema import validate, ValidationError

class MenuItem(Base):
    __tablename__ = TableNames.MENU_ITEM.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_item = Column(JSONB, nullable=False)

    SCHEMA = {
        'type' : 'object',
        'properties' : {
            'menu_items' : {
                'type' : 'array',
                'items' : {
                    'type' : 'object',
                    'properties' : {
                        'menu_id' : {
                            'type' : 'integer'
                        },
                        'name' : {
                            'type' : 'string'
                        },
                        'item_type' : {
                            'type' : 'string',
                            'enum' : ['appetizer', 'entree', 'dessert', 'drink', 'premade', 'addon']
                        },
                        'price' : {
                            'type' : 'number'
                        },
                        'ingredients' : {
                            'type' : 'array',
                            'items' : {
                                'type' : 'string'
                            }
                        }
                    },
                    'required' : ['name', 'item_type', 'price']
                }
            }
        },
        'required' : ['menu_items']
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
