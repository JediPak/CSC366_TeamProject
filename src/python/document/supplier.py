from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSON

from document import Base, TableNames

from jsonschema import validate, ValidationError

class Supplier(Base):
    __tablename__ = TableNames.SUPPLIER.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier = Column(JSON, nullable=False)

    SCHEMA = {
        'type' : 'object',
        'properties' : {
            'address' : {
                'type' : 'object',
                'properties' : {
                    'street_number' : { 'type' : 'number' },
                    'street_name' : { 'type' : 'string' },
                    'city' : { 'type' : 'string' },
                    'state' : { 'type' : 'string' },
                    'zip' : { 'type' : 'number' }
                }
            }
        }
    }

    @staticmethod
    def factory(json_dict):
        try:
            validate(json_dict, Supplier.SCHEMA)
            return Supplier(
                supplier=json_dict
            )
        except ValidationError:
            return None
