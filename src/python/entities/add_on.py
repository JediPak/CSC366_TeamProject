from sqlalchemy import Column, Integer, String, Date, Float

from entities import Base, TableNames
from order import MenuItem, ItemType

import enum

class AddOn(MenuItem):
    __tablename__ = TableNames.ADD_ON.value

    add_on_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(enum.Enum(ItemType), nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)

    def __repr__(self):
        return "AddOn(id={}, name={}, type={}, price={})".format(
            self.add_on_id,
            self.name,
            self.type,
            self.price
        )

    __mapper_args__ = {
        'polymorphic_identity': 'add_on',
        'concrete': True
    }