from sqlalchemy import Column, Integer, String, Date, Decimal

from entities import Base

import enum


class AddOnType(enum.Enum):
    TOPPING = 0   # ex. olives
    SAUCE = 1     # ex. ranch
    MEAT = 2      # ex. bacon


class AddOn(Base):
    __tablename__ = 'addOn'

    add_on_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(AddOnType), nullable=False)
    price = Column(Decimal, nullable=False)

    def __repr__(self):
        return "AddOn(id={}, name={}, type={}, price={})".format(
            self.add_on_id,
            self.name,
            self.type,
            self.price
        )
