from sqlalchemy import Column, Integer, String, ForeignKey

from entities import Base
from main_dish import MainDish
from ingredient import Ingredient

class DishIngredient(Base):
    __tablename__ = 'dishIngredient'

    ingredient_id = Column(Integer, ForeignKey(Ingredient.id), primary_key=True)
    main_dish_id = Column(Integer, ForeignKey(MainDish.id), primary_key=True)



    def __repr__(self):
        return "DishIngredient(ingredient_id={}, main_dish_id={})".format(
            self.ingredient_id,
            self.main_dish_id
        )
