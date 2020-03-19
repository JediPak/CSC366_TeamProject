from sqlalchemy import Column, Integer, String, ForeignKey

from entities import Base
from add_on import AddOn
from ingredient import Ingredient

class AddOnIngredient(Base):
    __tablename__ = 'addOnIngredient'

    ingredient_id = Column(Integer, ForeignKey(Ingredient.id), primary_key=True)
    add_on_id = Column(Integer, ForeignKey(AddOn.id), primary_key=True)



    def __repr__(self):
        return "AddOnIngredient(ingredient_id={}, add_on_id={})".format(
            self.ingredient_id,
            self.add_on_id
        )
