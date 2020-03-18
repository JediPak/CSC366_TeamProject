from sqlalchemy import *
from sqlalchemy.orm import relationship
from entities import Base

class LineItem(Base):
    __tablename__= 'lineItem'

    ordinal = Column(Integer, primary_key=True)

    def __repr__(self):
        return (
            'LineItem(ordinal={})'
        ).format(
            self.ordinal
        )

