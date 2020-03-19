from sqlalchemy import Column, Integer, String, Date, Decimal

from entities import Base

import enum

class PremadeType(enum.Enum):
    FROZEN = 0  # ex. frozen salisbury steak
    DRY = 1     # ex. tortilla chips
    CANNED = 2  # ex. chili sauce


class PremadeItem(Base):
    __tablename__ = 'premadeItem'

    premade_item_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(PremadeType), nullable=False)
    price = Column(Decimal, nullable=False)
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
