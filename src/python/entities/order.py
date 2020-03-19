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
    __tablename__ = 'menuItem'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    item_type = Column(Enum(ItemType), nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)

    UniqueConstraint(name)

    __mapper_args__ = {
        'polymorphic_identity':'menuItem',
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
    __tablename__ = 'receipt'

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
    __tablename__= 'lineItem'

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
