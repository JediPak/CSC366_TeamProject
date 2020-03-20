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

    def __repr__(self):
        return (
            'Receipt(receipt={}, time={})'
        ).format(
            self.receipt_number,
            self.time
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

addon_ingredient_association_table = Table('addon_ingredient_association', 
    Base.metadata,
    Column('addon_id', Integer, ForeignKey('addOn.add_on_id')),
    Column('ingredient_id', Integer, ForeignKey('ingredient.ingredient_id'))
)

maindish_ingredient_association_table = Table('maindish_ingredient_association',
    Base.metadata,
    Column('main_dish_id', Integer, ForeignKey('mainDish.main_dish_id')),
    Column('ingredient_id', Integer, ForeignKey('ingredient.ingredient_id')),
)

class AddOn(MenuItem):
    __tablename__ = TableNames.ADD_ON.value

    add_on_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(ItemType), nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)
    ingredients = relationship(
        "Ingredient",
        secondary=addon_ingredient_association_table,
        back_populates="addons"
    )

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
    ingredients = relationship(
        "Ingredient",
        secondary=maindish_ingredient_association_table,
        back_populates="main_dishes"
    )

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

class Ingredient(Base):
    __tablename__ = TableNames.INGREDIENT.value

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    addons = relationship(
        "AddOn",
        secondary=addon_ingredient_association_table,
        back_populates="ingredients"
    )
    main_dishes = relationship(
        "MainDish",
        secondary=maindish_ingredient_association_table,
        back_populates="ingredients"
    )

    def __repr__(self):
        return "Ingredient(id={}, name={})".format(
            self.ingredient_id,
            self.name
        )
