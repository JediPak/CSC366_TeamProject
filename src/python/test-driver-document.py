from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from document import Base
from document.branch import Branch
from document.menu_item import MenuItem
from document.receipt import Receipt
from document.supplier import Supplier
from document.invoice import Invoice
from document.employee import Employee
from document.pay import Pay

import unittest

class TestDBSetup(unittest.TestCase):

    def setUp(self):
        engine = create_engine(
            'postgresql://postgres:testtest@db.caoodninwjvh.us-east-2.rds.amazonaws.com:5432/postgres',
            echo=True
        )

        #Base.metadata.drop_all(engine)
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

    def test_add_supplier(self):
        supplier_json = {
            'manager_id' : 1,
            'address' : {
                'street_number' : 1,
                'street_name' : "Grand Ave.",
                'city' : "San Luis Obispo",
                'state' : "CA",
                'zip' : 93410
            }
        }

        supplier = Supplier.factory(supplier_json)
        self.assertIsNotNone(supplier)
        self.this_session.add(supplier)
        self.this_session.flush()

    def test_add_menu_item(self):
        menu_item_json = {
            'menu_items' : [
                {
                    'name' : 'Enchilada',
                    'item_type' : 'entree',
                    'price' : '10.50',
                    'ingredients' : [
                        'Rice',
                        'Cheese'
                    ]
                },
                {
                    'name' : 'Salsa',
                    'item_type' : 'addon',
                    'price' : '3.50',
                    'ingredients' : [
                        'Tomatoes', 
                        'Onion',
                        'Jalapeno'
                    ]
                },
                {
                    'name' : 'Chips',
                    'item_type' : 'premade',
                    'price' : '2.00'
                },
                {
                    'name' : 'Cola',
                    'item_type' : 'drink',
                    'price' : '1.00'
                }
            ]
        }

        menu_item = MenuItem.factory(menu_item_json)
        self.assertIsNotNone(menu_item)
        self.this_session.add(menu_item)
        self.this_session.flush()        

    def test_create_receipt(self):
        receipt_json = {
            'number' : 1,
            'time' : "10/10/10",
            'branch_id' : 1,
            'line_items' : [
                1,
                2
            ]
        }
        receipt = Receipt.factory(receipt_json)
        self.assertIsNotNone(receipt)
        self.this_session.add(receipt)
        self.this_session.flush()

    def test_add_invoice(self):
        invoice_json = {
            'invoice_id' : 1,
            'supplier_id' : 1,
            'branch_id' : 1,
            'order_date' : '2019-01-01',
            'deliver_date' : '2019-01-08',
            'items' : [
                {
                    'item_id' : 1,
                    'quantity' : 2,
                    'price' : 3.50
                },
                {
                    'item_id' : 2,
                    'quantity' :3,
                    'price' : 4.20
                },
            ]
        }

        invoice = Invoice.factory(invoice_json)
        self.assertIsNotNone(invoice)
        self.this_session.add(invoice)
        self.this_session.flush()

    def test_add_pay(self):
        pay_json = {
            'pay_id' : 1,
            'payperiod' : '01-07-2020',
            'emp_role_id' : 2,
            'time_cards' :
            [
                [
                    '01-07-2020',
                    True,
                    [
                        ['01-07-2020', 'REGULAR', 8],
                        ['01-09-2020', 'REGULAR', 8]
                    ]
                ],
                [
                    '01-14-2020',
                    True,
                    [
                        ['01-14-2020', 'REGULAR', 8],
                        ['01-16-2020', 'PTO', 8]
                    ]
                ]
            ]

        }

        pay = Pay.factory(pay_json)
        self.assertIsNotNone(pay)
        self.this_session.add(pay)
        self.this_session.flush()

if __name__ == '__main__':
    unittest.main()
