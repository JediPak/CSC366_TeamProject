from sqlalchemy import Column, Integer, String, ForeignKey

from entities import Base, TableNames

class AddOnIngredient(Base):
    __tablename__ = TableNames.ADD_ON_INGREDIENT.value

    ingredient_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.INGREDIENT.value),default=None), primary_key=True)
    add_on_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.ADD_ON.value),default=None), primary_key=True)


    def __repr__(self):
        return "AddOnIngredient(ingredient_id={}, add_on_id={})".format(
            self.ingredient_id,
            self.add_on_id
        )
