from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from document import Base, TableNames

from jsonschema import validate, ValidationError

class Pay(Base):
    __tablename__ = TableNames.PAY.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    pay = Column(JSONB, nullable=False)

    SCHEMA = {
        'type' : 'object',
        'properties' : {
            'pay_id' : { 'type' : 'number' },
            'payperiod' : { 'type' : 'string' },
            'emp_role_id' : { 'type' : 'number' },
            'time_cards':{
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": 
                                [
                                {"type": "string"}, 
                                {"type": "boolean"}, 
                                {"type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": 
                                            [
                                                {"type": "string"}, 
                                                {
                                                    "type": "string",
                                                    "enum": ["REGULAR", "OVERTIME", "PTO"]
                                                }, 
                                                {"type": "number"} 
                                            ]}
                                }]
                            }
                        }
        }
    }

    @staticmethod
    def factory(json_dict):
        try:
            validate(json_dict, Pay.SCHEMA)
            return Pay(
                pay=json_dict
            )
        except ValidationError:
            return None
