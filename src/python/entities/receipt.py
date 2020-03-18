from sqlalchemy import *
from sqlalchemy.orm import relationship
from entities import Base


class Receipt(Base):
    __tablename__ = 'receipt'

    receipt_number = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return (
            'Receipt(receipt={}, time={})'
        ).format(
            self.receipt_number,
            self.time
        )


