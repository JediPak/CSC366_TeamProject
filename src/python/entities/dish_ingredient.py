from sqlalchemy import Column, Integer, String, ForeignKey

from entities import Base, TableNames


class DishIngredient(Base):
    __tablename__ = TableNames.DISH_INGREDIENT.value

    ingredient_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.INGREDIENT.value),default=None), primary_key=True)
    main_dish_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.MAIN_DISH.value),default=None), primary_key=True)


    def __repr__(self):
        return "DishIngredient(ingredient_id={}, main_dish_id={})".format(
            self.ingredient_id,
            self.main_dish_id
        )
