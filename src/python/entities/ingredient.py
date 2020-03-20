from sqlalchemy import Column, Integer, String

from entities import Base, TableNames


class Ingredient(Base):
    __tablename__ = TableNames.INGREDIENT.value

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    

    def __repr__(self):
        return "Ingredient(id={}, name={})".format(
            self.ingredient_id,
            self.name
        )
