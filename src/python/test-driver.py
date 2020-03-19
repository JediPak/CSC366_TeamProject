import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities import Base
from entities.store import Store
from entities.supplier import Supplier
from entities.invoice import Invoice
from entities.branch import Branch
from entities.employee import *
from entities.pay import PayCheck, TimeCard, Entry, HourType

from datetime import date

class TestDBSetup(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        session = sessionmaker()
        session.configure(bind=engine)
        self.this_session = session()

    def test_add_store(self):
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

    def test_add_supplier(self):
        address = '1 Grand Ave'
        city = 'San Luis Obispo'
        state = 'CA'
        zip_code = 93410
        new_supplier = Supplier(
            address=address,
            city=city,
            state=state,
            zip_code=zip_code
        )
        self.this_session.add(new_supplier)

        out_supplier = self.this_session.query(Supplier).filter_by(supplier_id=1).first()
        self.assertEqual(out_supplier.address, address)
        self.assertEqual(out_supplier.city, city)
        self.assertEqual(out_supplier.state, state)
        self.assertEqual(out_supplier.zip_code, zip_code)

    def test_add_invoice(self):
        supplier = 1
        branch = 1
        new_invoice = Invoice(
            supplier=supplier,
            branch=branch
        )
        self.this_session.add(new_invoice)

        out_invoice = self.this_session.query(Invoice).filter_by(invoice_id=1).first()
        self.assertEqual(out_invoice.supplier, 1)
        self.assertEqual(out_invoice.branch, 1)

if __name__ == '__main__':
    unittest.main()
