from sqlalchemy import *
from sqlalchemy.orm import relationship

from entities import Base

import enum

class Exemption(enum.Enum):
    EXEMPT = 0
    NON_EXEMPT = 1

class RoleName(enum.Enum):
    PRESIDENT = 0
    REGIONAL_MANAGER = 1
    BRANCH_MANAGER = 2
    CHEF = 3
    PREP_CHEF = 4
    DISHWASHER = 5

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(Enum(RoleName), nullable=False)
    type = Column(Enum(Exemption), nullable=False)
    # TODO how does this precision work
    rate = Column(Float(precision='7,2'), nullable=False)
    UniqueConstraint(name)
    CheckConstraint('rate >= 15.00')

    def __repr__(self):
        return 'Role(id={}, name={}, type={}, rate={})'.format(
            self.id,
            self.name,
            self.type,
            self.rate
        )

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    #emp_id = Column(Integer, nullable=False)
    ssn = Column(Integer)
    name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    manager_id = Column(Integer, ForeignKey('employee.id'))
    role_id = Column(Integer, ForeignKey('role.id'))
    
    manager = relationship('Employee', remote_side=[id])
    role = relationship('Role')

    UniqueConstraint(ssn, start_date)

    def __repr__(self):
        return (
            'Employee(id={}, ssn={}, name={}, ' +
            'role={}, start={}, end={}, manager={})'
        ).format(
            self.id,
            self.ssn,
            self.name,
            self.role,
            self.start_date,
            self.end_date,
            self.manager
        )
