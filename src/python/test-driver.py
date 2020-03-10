import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities.store import Store, Base

class TestDBSetup(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        session = sessionmaker()
        session.configure(bind=engine)
        self.this_session = session()
        

    def test1(self):
        address = '1 Grand Ave'
        city = 'San Luis Obispo'
        state = 'CA'
        zip_code = 93410
        new_store = Store(
            address=address, 
            city=city, 
            state=state, 
            zip_code=zip_code
        )
        self.this_session.add(new_store)

        out_store = self.this_session.query(Store).filter_by(store_id=1).first() 
        self.assertEqual(out_store.address, address)
        self.assertEqual(out_store.city, city)
        self.assertEqual(out_store.state, state)
        self.assertEqual(out_store.zip_code, zip_code)

if __name__ == '__main__':
    unittest.main()