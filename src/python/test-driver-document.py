from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from document import Base
from document.branch import Branch
from document.employee import Employee

import unittest

class TestDBSetup(unittest.TestCase):

    def setUp(self):
        engine = create_engine(
            'postgresql://postgres:testtest@db.caoodninwjvh.us-east-2.rds.amazonaws.com:5432/postgres', 
            echo=True
        )
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session = sessionmaker()
        session.configure(bind=engine)
        self.this_session = session()

    def test_add_employee(self):
        branch_json = {
            'branches' : [
                {
                    'branch_id' : 1,
                    'manager_id' : 1,
                    'address' : {
                        'street_number' : 1,
                        'street_name' : "Grand Ave.",
                        'city' : "San Luis Obispo",
                        'state' : "CA",
                        'zip' : 93410
                    }
                }
            ]
        }

        employee_json = {
            'emp_id' : 1,
            'ssn' : 555555555,
            'name' : {
                'first' : 'Tyler',
                'last' : 'Davis',
                'title' : 'Mr.'
            },
            'roles' : [
                {
                    'role' : 'Chef',
                    'exempt' : False,
                    'pay' : 20.00,
                    'start' : '2020-03-12',
                    'end' : '2020-03-18',
                    'branch_id' : 1
                },
                {
                    'role' : 'Branch Manager',
                    'exempt' : True,
                    'pay' : 3000.00,
                    'start' : '2020-03-19',
                    'end' : None,
                    'branch_id' : 1
                }
            ]
        }

        branch = Branch.factory(branch_json)
        emp = Employee.factory(employee_json)
        self.assertIsNotNone(branch)
        self.assertIsNotNone(emp)
        self.this_session.add_all((branch,emp))
        self.this_session.flush()
        
if __name__ == '__main__':
    unittest.main()
    