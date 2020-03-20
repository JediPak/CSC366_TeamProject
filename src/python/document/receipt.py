from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from document import Base, TableNames

from jsonschema import validate, ValidationError

class Receipt(Base):
    __tablename__ = TableNames.RECEIPT.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt = Column(JSONB, nullable=False)

    SCHEMA = {
        'type' : 'object',
        'properties' : {
            'number' : {
                'type' : 'number'
            },
            'time' : {
                'type' : 'string'
            },
            'branch_id' : {
                'type' : 'integer'
            },
            'line_items' : { 
                'type' : 'array',
                'items' : {
                    'type' : 'object',
                    'properties' : {
                        'menu_id' : {
                            'type' : 'integer'
                        }
                    }
                }
            }
        },
        'required' : [
            'number',
            'time',
            'branch_id'
            ]
    }

    @staticmethod
    def factory(json_dict):
        try:
            validate(json_dict, Receipt.SCHEMA)
            return Receipt(
                receipt = json_dict
            )
        except ValidationError:
            return None
                    
