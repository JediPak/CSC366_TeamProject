from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from document import Base, TableNames

from jsonschema import validate, ValidationError

class Branch(Base):
    __tablename__ = TableNames.BRANCH.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    branch = Column(JSONB, nullable=False)

    BRANCH_SCHEMA = {
        'type' : 'object',
        'properties' : {
            'branch_id' : { 'type' : 'number' },
            'manager_id' : { 'type' : 'number' },
            'address' : {
                'type' : 'object',
                'properties' : {
                    'street_number' : { 'type' : 'number' },
                    'street_name' : { 'type' : 'string' },
                    'city' : { 'type' : 'string' },
                    'state' : { 'type' : 'string' },
                    'zip' : { 'type' : 'number' }
                },
                'required' : ['street_number', 'street_name', 'city', 'state', 'zip']
            }
        },
        'required' : ['branch_id', 'address', 'manager_id']
    }

    SCHEMA = {
        'type' : 'object',
        'properties' : {
            'branches' : {
                'type' : 'array',
                'minItems' : 1,
                "uniqueItems" : True,
                'items' : BRANCH_SCHEMA
            }
        }
    }

    @staticmethod
    def factory(json_dict):
        try:
            validate(json_dict, Branch.SCHEMA)
            return Branch(
                branch=json_dict
            )
        except ValidationError:
            return None
