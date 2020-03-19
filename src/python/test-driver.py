import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities import Base
from entities.order import *

from datetime import date

class TestDBSetup(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        session = sessionmaker()
        session.configure(bind=engine)
        self.this_session = session()
        
    def test_create_receipt(self):
        receipt = Receipt()
        name = "Pasta"
        price=13.20
        menu_item = MenuItem(
            name=name, 
            item_type = ItemType.ENTREE,
            price=price
        )
        ordinal = 1
        line_item = LineItem(
            ordinal=ordinal,
            receipt=receipt,
            menu_item=menu_item
        )

        name = "Enchiladas"
        price=20.00
        menu_item = MenuItem(
            name=name, 
            item_type = ItemType.ENTREE,
            price=price
        )

        ordinal = 2
        line_item = LineItem(
            ordinal=ordinal,
            receipt=receipt,
            menu_item=menu_item
        )

        self.this_session.add_all(
                (receipt, menu_item, line_item)
        )
        self.this_session.flush()

if __name__ == '__main__':
    unittest.main()
