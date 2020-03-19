from sqlalchemy import *
from sqlalchemy.orm import relationship

from entities import Base

class TimeCard(Base):
    __tablename__ = 'timeCard'

    id = Column(Integer, primary_key=True)
    weekOf = Column(Date, nullable=False)
    isApproved = Column(BOOLEAN, nullable=False)

    paycheck_id = Column(Integer, ForeignKey('paycheck.id'))

    def __repr__(self):
        return (
            'TimeCard(id={}, weekOf={}, isApproved={})'
        ).format(
            self.id,
            self.weekOf,
            self.isApproved
        )
