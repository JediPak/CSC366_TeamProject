from sqlalchemy import Column, Integer, String, Date, Float

from entities import Base

import enum
from menu_item import MenuItem

class PremadeItem(MenuItem):
    __tablename__ = 'premadeItem'

    premade_item_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(enum.Enum(ItemType), nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)
    sell_by = Column(Date, nullable=False)
    packaged_on = Column(Date, nullable=False)

    def __repr__(self):
        return "PremadeItem(id={}, name={}, type={}, price={}, sell_by={}, packaged_on={})".format(
            self.premade_item_id,
            self.name,
            self.type,
            self.price,
            self.sell_by,
            self.packaged_on
        )

    __mapper_args__ = {
        'polymorphic_identity': 'premade_item',
        'concrete': True
    }
