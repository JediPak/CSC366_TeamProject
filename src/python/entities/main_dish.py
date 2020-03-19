from sqlalchemy import Column, Integer, String, Date, Decimal

from entities import Base

import enum

class MainDishType(enum.Enum):
    ENTREE = 0        # ex. grilled chicken
    APPETIZER = 1     # ex. jalapeno poppers
    DESSERT = 2       # ex. chocolate lava cake


class MainDish(Base):
    __tablename__ = 'mainDish'

    main_dish_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(MainDishType), nullable=False)
    price = Column(Decimal, nullable=False)

    def __repr__(self):
        return "MainDish(id={}, name={}, type={}, price={})".format(
            self.main_dish_id,
            self.name,
            self.type,
            self.price
        )
