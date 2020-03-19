from sqlalchemy import *
from sqlalchemy.orm import relationship

from entities import Base, TableNames

import datetime
import enum

class PayCheck(Base):
    __tablename__ = TableNames.PAYCHECK.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    payperiod = Column(Date, nullable=False, default=datetime.datetime.now)

    emp_role_id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.EMPLOYEE.value)), 
        nullable=False
    )

    UniqueConstraint(payperiod, emp_role_id)

    emp_role = relationship('Employee')

    def __repr__(self):
        return 'Paycheck(id={}, payperiod={}, emp={})'.format(
            self.id,
            self.payperiod,
            self.emp_role
        )

class TimeCard(Base):
    __tablename__ = TableNames.TIME_CARD.value
    WEEKS_PER_CHECK = 2 

    id = Column(Integer, primary_key=True, autoincrement=True)
    week_of = Column(Date, nullable=False, default=datetime.datetime.now)
    is_approved = Column(Boolean, nullable=False, default=False)

    paycheck_id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.PAYCHECK.value)),
        nullable=False
    )

    UniqueConstraint(week_of, paycheck_id)

    paycheck = relationship('PayCheck')

    weeks_trigger = DDL(
        '''
        delimiter //
        CREATE TRIGGER manager_check BEFORE INSERT ON {table}
        FOR EACH ROW
        BEGIN
            IF (
                SELECT
                    count(*)
                FROM
                    {table}
                WHERE
                    end_date IS NULL AND
                    manager_id = NEW.manager_id
            ) >= {weeks} THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '{weeks} of timecards per paycheck';
            END IF;
        END;//
        delimiter ;
        '''.format(
            table=TableNames.TIME_CARD.value,
            weeks=WEEKS_PER_CHECK
        )
    )

    def __repr__(self):
        return (
            'TimeCard(id={}, weekOf={}, is_approved={})'
        ).format(
            self.id,
            self.weekOf,
            self.isApproved
        )

class HourType(enum.Enum):
    REGULAR = 0
    OVERTIME = 1
    PTO = 2

class Entry(Base):
    __tablename__ = TableNames.TIME_CARD_ENTRY.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, default=datetime.datetime.now)
    hour_type = Column(Enum(HourType), nullable=False)
    hours = Column(Integer, nullable=False)

    timecard_id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.TIME_CARD.value)),
        nullable=False
    )

    UniqueConstraint(date, hour_type)

    timecard = relationship('TimeCard')
    
    def __repr__(self):
        return (
            'Entry(id={}, date={}, hour_type={}, ' +
            'hours={}, timecard={})'
        ).format(
            self.id,
            self.date,
            self.hour_type,
            self.hours,
            self.timecard
        )
