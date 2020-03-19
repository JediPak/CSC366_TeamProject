from sqlalchemy import *
from sqlalchemy.orm import relationship

from entities import Base


class HourType(enum.Enum):
    REGULAR = 0
    OVERTIME = 1
    PTO = 2

class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    hour_type = Column(Enum(HourType), nullable=False)
    hours = Column(Integer, nullable=False)

    timeCard_id = Column(Integer, ForeignKey('timecard.id'))
    

    def __repr__(self):
        return (
            'Entry(id={}, date={}, hour_type={}, ' +
            'hours={}, timeCard_id={})'
        ).format(
            self.id,
            self.date,
            self.hour_type,
            self.hours,
            self.timeCard_id
        )
