from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from document import Base, TableNames

from jsonschema import validate, ValidationError

import enum
import datetime

class Employee(Base):
    __tablename__ = TableNames.EMPLOYEE.value
    MAX_MANAGES = 20

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp = Column(JSONB, nullable=False)

    ROLE_SCHEMA = {
        'type' : 'object',
        'properties' : {
            'role' : {
                'type' : 'string',
                'enum' : ['CEO', 'Board Member', 'President', 'Regional Manager', 'Branch Manager', 'Server', 'Chef', 'Dishwasher']
            },
            'exempt' : { 'type' : 'boolean' },
            'pay' : { 'type' : 'number' },
            'start' : { 'type' : 'string' },
            'end' : { 'type' : ['string', 'null'] },
            'manager_emp_id' : { 'type' : 'number' },
            'branch_id' : { 'type' : 'number' }
        },
        'required' :  ['role', 'exempt', 'pay', 'start', 'end']
    }

    SCHEMA = {
        'type' : 'object',
        'properties' : {
            'emp_id' : { 'type' : 'number' },
            'ssn' : { 'type' : 'number' },
            'name' : {
                'type' : 'object',
                'properties' : {
                    'first' : { 'type' : 'string' },
                    'last' : { 'type' : 'string' },
                    'suffix' : { 'type' : 'string' },
                    'title' : { 'type' : 'string' }
                }
            },
            'roles' : {
                'type' : 'array',
                'minItems' : 1,
                'items' : ROLE_SCHEMA
            }
        },
        'required' : ['emp_id', 'ssn', 'name', 'roles']
    }

    @staticmethod
    def factory(json_dict):
        try:
            validate(json_dict, Employee.SCHEMA)
            nones = len(
                list(
                    filter(
                        lambda end: end is None, 
                        map(
                            lambda role: role['end'], 
                            json_dict['roles']
                        )
                    )
                )
            )
            assert(
                (nones == 1 and json_dict['roles'][-1]['end'] is None) or
                nones == 0
            )
            return Employee(
                emp=json_dict
            )
        except ValidationError:
            return None
        except AssertionError:
            return None
