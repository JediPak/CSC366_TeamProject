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

class Item(Base):
    __tablename__ = TableNames.ITEM.value

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    UniqueConstraint(name)

    def __repr__(self):
        return (
            'Item(id={}, name={})'
        ).format(
            self.id,
            self.name
        )


class MenuItem(Item):
    __tablename__ = TableNames.MENU_ITEM.value
    
    id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.ITEM.value)), 
        primary_key=True
    )

    item_type = Column(Enum(ItemType), nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)
    type = Column(String(30), nullable=False)

    __mapper_args__ = {
        'polymorphic_on':type
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

dish_ingredient_association_table = Table('dish_ingredient_association',
    Base.metadata,
    Column('dish_id', Integer, ForeignKey('{}.id'.format(TableNames.MENU_ITEM.value))),
    Column('ingredient_id', Integer, ForeignKey('{}.id'.format(TableNames.INGREDIENT.value))),
)

class AddOn(MenuItem):
    __tablename__ = TableNames.ADD_ON.value

    id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.MENU_ITEM.value)), 
        primary_key=True
    )

    ingredients = relationship(
        "Ingredient",
        secondary=dish_ingredient_association_table,
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
        'polymorphic_identity': 'add_on'
    }


class MainDish(MenuItem):
    __tablename__ = TableNames.MAIN_DISH.value

    id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.MENU_ITEM.value)), 
        primary_key=True
    )
    ingredients = relationship(
        "Ingredient",
        secondary=dish_ingredient_association_table,
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
        'polymorphic_identity': 'main_dish'
    }


class PremadeItem(MenuItem):
    __tablename__ = TableNames.PREMADE_ITEM.value

    id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.MENU_ITEM.value)), 
        primary_key=True
    )

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
        'polymorphic_identity': 'premade_item'
    }

class Ingredient(Item):
    __tablename__ = TableNames.INGREDIENT.value

    id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.ITEM.value)), 
        primary_key=True
    )

    addons = relationship(
        "AddOn",
        secondary=dish_ingredient_association_table,
        back_populates="ingredients"
    )
    main_dishes = relationship(
        "MainDish",
        secondary=dish_ingredient_association_table,
        back_populates="ingredients"
    )

    def __repr__(self):
        return "Ingredient(id={}, name={})".format(
            self.ingredient_id,
            self.name
        )