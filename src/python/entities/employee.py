from sqlalchemy import *
from sqlalchemy.orm import relationship

from entities import Base, TableNames

import enum
import datetime

class Exemption(enum.Enum):
    EXEMPT = 0
    NON_EXEMPT = 1

class RoleName(enum.Enum):
    CEO = 0
    BOARD_MEMBER = 1
    PRESIDENT = 2
    REGIONAL_MANAGER = 3
    BRANCH_MANAGER = 4
    CHEF = 5
    PREP_CHEF = 6
    DISHWASHER = 7

class Role(Base):
    __tablename__ = TableNames.ROLE.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(RoleName), nullable=False)
    type = Column(Enum(Exemption), nullable=False)
    rate = Column(Float(precision='7,2'), CheckConstraint('rate >= 15.00'), nullable=False)
    UniqueConstraint(name)

    def __repr__(self):
        return 'Role(id={}, name={}, type={}, rate={})'.format(
            self.id,
            self.name,
            self.type,
            self.rate
        )

class EmployeeInfo(Base):
    __tablename__ = TableNames.EMPLOYEE_INFO.value

    emp_id = Column(Integer, primary_key=True, autoincrement=True)
    ssn = Column(Integer, nullable=False, unique=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return (
            'EmployeeInfo(emp_id={}, ssn={}, name={})'
        ).format(
            self.emp_id,
            self.ssn,
            self.name
        )

class Employee(Base):
    __tablename__ = TableNames.EMPLOYEE.value
    MAX_MANAGES = 20

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, nullable=False, default=datetime.datetime.utcnow)
    end_date = Column(Date, default=None)

    manager_id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.EMPLOYEE.value)),
        default=None
    )
    role_id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.ROLE.value)), 
        nullable=False
    )
    emp_id = Column(
        Integer, 
        ForeignKey('{}.emp_id'.format(TableNames.EMPLOYEE_INFO.value)), 
        nullable=False
    )
    works_at_id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.BRANCH.value))
    )

    manager = relationship('Employee', remote_side=[id])
    role = relationship('Role')
    emp = relationship('EmployeeInfo')
    works_at = relationship('Branch', foreign_keys=[works_at_id], post_update=True)

    UniqueConstraint(emp_id, start_date)

    manager_trigger = DDL(
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
            ) >= {max_manages} THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Employee may not manage more than {max_manages} people';
            END IF;

            IF EXISTS(
                SELECT
                    count(*)
                FROM
                    {table}
                WHERE
                    end_date IS NULL AND
                    emp_id = NEW.emp_id
            ) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Employee may hold only one role';
            END IF;
        END;//
        delimiter ;
        '''.format(
            table=TableNames.EMPLOYEE.value,
            max_manages=MAX_MANAGES
        )
    )

    def __repr__(self):
        return (
            'Employee(id={}, start={}, end={}, emp={}, role={}, manager={})'
        ).format(
            self.id,
            self.start_date,
            self.end_date,
            self.emp,
            self.role,
            self.manager
        )
