from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from document import Base, TableNames

from jsonschema import validate, ValidationError

class Invoice(Base):
    __tablename__ = TableNames.INVOICE.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice = Column(JSONB, nullable=False)

    SCHEMA = {
        'type' : 'object',
        'properties' : {
            'invoice_id' : {'type' : 'number'},
            'supplier_id' : {'type' : 'number'},
            'branch_id' : {'type' : 'number'},
            'order_date' : {'type' : 'string'},
            'deliver_date' : {'type' : 'string'},
            'items' : {'type' : 'array',
                'minItems': 1,
                'uniqueItems': 'true',
                    'list_items' : {'type' : 'object',
                        'item_id' : {'type' : 'number'},
                        'quantity' : {'type' : 'number'},
                        'price' : {'type' : 'number'},
                    }
            }
        },
        'required' : ['invoice_id', 'supplier_id', 'branch_id', 'order_date', 'items']
    }

    @staticmethod
    def factory(json_dict):
        try:
            validate(json_dict, Invoice.SCHEMA)
            return Invoice(
                invoice=json_dict
            )
        except ValidationError:
            return None
