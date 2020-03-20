from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSON

from document import Base, TableNames

from jsonschema import validate, ValidationError

class LineItem(Base):
    __tablename__ = TableNames.LINE_ITEM.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_item = Column(JSON, nullable=False)

    SCHEMA = {
        'type' : 'object',
        'properties' : {
            'ordinal' : {
                'type' : 'number'
            }
        }
    }

    @staticmethod
    def factory(json_dict):
        try:
            validate(json_dict, LineItem.SCHEMA)
            return LineItem(
                line_item = json_dict
            )
        except ValidationError:
            return None
                    
