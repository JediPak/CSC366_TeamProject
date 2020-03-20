from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from document import Base
from document.branch import Branch
from document.menu_item import MenuItem


import unittest

class TestDBSetup(unittest.TestCase):

    def setUp(self):
        engine = create_engine(
            'postgresql://postgres:testtest@db.caoodninwjvh.us-east-2.rds.amazonaws.com:5432/postgres', 
            echo=True
        )
        # Base.metadata.drop_all(engine)
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

    def test_add_menu_item(self):
        menu_item_json = {
            'items' : [
                {
                    'name' : 'Enchilada',
                    'item_type' : 'entree',
                    'price' : '10.50',
                    'ingredients' : [
                        {
                            'name' : 'Rice'
                        },
                        {
                            'name' : 'Cheese'
                        }
                    ]
                },
                {
                    'name' : 'Salsa',
                    'item_type' : 'addon',
                    'price' : '3.50',
                    'ingredients' : [
                        {
                            'name' : 'Tomatoes'
                        },
                        {
                            'name' : 'Onion'
                        }
                    ]
                },
                {
                    'name' : 'Chips',
                    'item_type' : 'premade',
                    'price' : '2.00'
                }
            ]
        }

        menu_item = MenuItem.factory(menu_item_json)
        self.assertIsNotNone(menu_item)
        self.this_session.add(menu_item)
        self.this_session.flush()        


if __name__ == '__main__':
    unittest.main()
    