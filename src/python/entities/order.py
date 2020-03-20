from sqlalchemy import *
from sqlalchemy.orm import relationship
from entities import Base, TableNames

import enum
import datetime

class ItemType(enum.Enum):
    APPETIZER = 0
    ENTREE = 1
    DESSERT = 2
    DRINK = 3
    PREMADE = 4
    ADDON = 5

class MenuItem(Base):
    __tablename__ = TableNames.MENU_ITEM.value
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    item_type = Column(Enum(ItemType), nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)

    UniqueConstraint(name)

    __mapper_args__ = {
        'polymorphic_identity':'menuItem',
    }

    def __repr__(self):
        return (
            'MenuItem(id={}, name={}, type={}, price={})'
        ).format(
            self.id,
            self.name,
            self.type,
            self.price
        )

class Receipt(Base):
    __tablename__ = TableNames.RECEIPT.value

    receipt_number = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.datetime.now)

    branch_id = Column(
        Integer,
        ForeignKey('{}.id'.format(TableNames.BRANCH.value)),
        nullable=False
    )

    branch = relationship('Branch')
    def __repr__(self):
        return (
            'Receipt(receipt={}, time={}, branch={})'
        ).format(
            self.receipt_number,
            self.time,
            self.branch
        )

class LineItem(Base):
    __tablename__= TableNames.LINE_ITEM.value

    id = Column(Integer, primary_key=True)
    ordinal = Column(Integer, nullable=False)

    receipt_id = Column(
        Integer,
        ForeignKey('{}.receipt_number'.format(TableNames.RECEIPT.value)),
        nullable=False
    )
    menu_id = Column(
        Integer,
        ForeignKey('{}.id'.format(TableNames.MENU_ITEM.value)),
        nullable=False
    )

    menu_item = relationship('MenuItem')
    receipt = relationship('Receipt')

    def __repr__(self):
        return (
            'LineItem(id={}, ordinal={}, menu_item={}, receipt={})'
        ).format(
            self.id,
            self.ordinal,
            self.menu_item,
            self.receipt
        )

class AddOn(MenuItem):
    __tablename__ = TableNames.ADD_ON.value

    add_on_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(ItemType), nullable=False)
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
    type = Column(Enum(ItemType), nullable=False)
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
    type = Column(Enum(ItemType), nullable=False)
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
