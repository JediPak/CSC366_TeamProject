from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from document import Base
from document.branch import Branch
from document.receipt import Receipt

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

    def test_add_store(self):
        branch_json = {
            'manager_id' : 1,
            'address' : {
                'street_number' : 1,
                'street_name' : "Grand Ave.",
                'city' : "San Luis Obispo",
                'state' : "CA",
                'zip' : 93410
            }
        }

        branch = Branch.factory(branch_json)
        self.assertIsNotNone(branch)
        self.this_session.add(branch)
        self.this_session.flush()

    def test_create_receipt(self):
        receipt_json = {
            'number' : 1,
            'time' : "10/10/10",
            'branch_id' : 1,
            'items' : [
                {
                    'ordinal' : 3,
                    'menu_id' : 1
                },
                {
                    'ordinal' : 4,
                    'menu_id' : 2
                }
            ]
        }
        receipt = Receipt.factory(receipt_json)
        self.assertIsNotNone(receipt)
        self.this_session.add(receipt)
        self.this_session.flush()

        
if __name__ == '__main__':
    unittest.main()
    
