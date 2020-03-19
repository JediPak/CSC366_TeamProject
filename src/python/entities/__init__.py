from sqlalchemy.ext.declarative import declarative_base

import enum

Base = declarative_base()

class TableNames(enum.Enum):
    ROLE = 'role'
    EMPLOYEE = 'employee'
    EMPLOYEE_INFO = 'employeeInfo'
    BRANCH = 'branch'
