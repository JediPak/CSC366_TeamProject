from sqlalchemy import *
from sqlalchemy.orm import relationship

from entities import Base


class Paycheck(Base):
    __tablename__ = 'paycheck'

    id = Column(Integer, primary_key=True)
    payperiod = Column(Date, nullable=False) #start wk of the 2 wk period

    #foreign key employee id

    def __repr__(self):
        return 'Paycheck(id={}, payperiod={})'.format(
            self.id,
            self.payperiod,

        )



