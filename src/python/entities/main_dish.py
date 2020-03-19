from sqlalchemy import Column, Integer, String, Date, Float

from entities import Base

import enum
from menu_item import MenuItem

class MainDish(MenuItem):
    __tablename__ = 'mainDish'

    main_dish_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(enum.Enum(ItemType), nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)

    def __repr__(self):
        return "MainDish(id={}, name={}, type={}, price={})".format(
            self.main_dish_id,
            self.name,
            self.type,
            self.price
        )

    __mapper_args__ = {
        'polymorphic_identity': 'main_dish',
        'concrete': True
    }