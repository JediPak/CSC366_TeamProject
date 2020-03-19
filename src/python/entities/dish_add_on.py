from sqlalchemy import Column, Integer, String, ForeignKey

from entities import Base
from add_on import AddOn
from main_dish import MainDish

class DishAddOn(Base):
    __tablename__ = 'dishAddOn'

    main_dish_id = Column(Integer, ForeignKey(MainDish.id), primary_key=True)
    add_on_id = Column(Integer, ForeignKey(AddOn.id), primary_key=True)



    def __repr__(self):
        return "DishAddOn(main_dish_id={}, add_on_id={})".format(
            self.main_dish_id,
            self.add_on_id
        )
