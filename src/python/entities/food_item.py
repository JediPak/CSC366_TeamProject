from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey

from entities import Base, TableNames
from order import MenuItem, ItemType

import enum


class AddOn(MenuItem):
    __tablename__ = TableNames.ADD_ON.value

    add_on_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(enum.Enum(ItemType), nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)

    def __repr__(self):
        return "AddOn(id={}, name={}, type={}, price={})".format(
            self.add_on_id,
            self.name,
            self.type,
            self.price
        )

    __mapper_args__ = {
        'polymorphic_identity': 'add_on',
        'concrete': True
    }


class MainDish(MenuItem):
    __tablename__ = TableNames.MAIN_DISH.value

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


class PremadeItem(MenuItem):
    __tablename__ = TableNames.PREMADE_ITEM.value

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


# joiner class between AddOns and Ingredients
class AddOnIngredient(Base):
    __tablename__ = TableNames.ADD_ON_INGREDIENT.value

    ingredient_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.INGREDIENT.value),default=None), primary_key=True)
    add_on_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.ADD_ON.value),default=None), primary_key=True)


    def __repr__(self):
        return "AddOnIngredient(ingredient_id={}, add_on_id={})".format(
            self.ingredient_id,
            self.add_on_id
        )


# joiner class between MainDishes and Ingredients
class DishIngredient(Base):
    __tablename__ = TableNames.DISH_INGREDIENT.value

    ingredient_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.INGREDIENT.value),default=None), primary_key=True)
    main_dish_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.MAIN_DISH.value),default=None), primary_key=True)


    def __repr__(self):
        return "DishIngredient(ingredient_id={}, main_dish_id={})".format(
            self.ingredient_id,
            self.main_dish_id
        )


# joiner class between AddOns and MainDishes
class DishAddOn(Base):
    __tablename__ = TableNames.DISH_ADD_ON.value

    main_dish_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.MAIN_DISH.value),default=None), primary_key=True)
    add_on_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.ADD_ON.value),default=None), primary_key=True)


    def __repr__(self):
        return "DishAddOn(main_dish_id={}, add_on_id={})".format(
            self.main_dish_id,
            self.add_on_id
        )
