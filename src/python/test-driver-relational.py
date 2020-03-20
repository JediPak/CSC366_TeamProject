import unittest

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from entities import Base
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
        event.listen(Employee.__table__, 'after_create', Employee.manager_trigger.execute_if(dialect="mysql"))
        event.listen(TimeCard.__table__, 'after_create', TimeCard.weeks_trigger.execute_if(dialect="mysql"))
        session = sessionmaker()
        session.configure(bind=engine)
        self.this_session = session()

    def test_add_employees(self):
        manager_role = Role(
            name=RoleName.BRANCH_MANAGER,
            type=Exemption.EXEMPT,
            rate=5000.00
        )
        managed_role = Role(
            name=RoleName.CHEF,
            type=Exemption.NON_EXEMPT,
            rate=20.00
        )
        branch = Branch(
            address='1 Grand Ave.',
            city='San Luis Obispo',
            state='CA',
            zip_code=93410
        )

        manager_ssn = 555555555
        manager_name = 'Joe'
        manager_info = EmployeeInfo(
            ssn=manager_ssn,
            name=manager_name
        )
        manager = Employee(
            emp=manager_info,
            role=manager_role,
            works_at=branch
        )
        branch.manager = manager

        managed_ssn = 444444444
        managed_name = 'Bill'
        managed_info = EmployeeInfo(
            ssn=managed_ssn,
            name=managed_name
        )
        managed = Employee(
            emp=managed_info,
            role=managed_role,
            manager=manager,
            works_at=branch
        )

        self.this_session.add_all(
            (manager_role, managed_role, branch, manager_info, manager, managed_info, managed)
        )
        self.this_session.flush()

    def test_add_paycheck(self):
        manager_role = Role(
            name=RoleName.CEO,
            type=Exemption.EXEMPT,
            rate=50000.00
        )

        manager_ssn = 555555555
        manager_name = 'Joe'
        manager_info = EmployeeInfo(
            ssn=manager_ssn,
            name=manager_name
        )
        manager = Employee(
            emp=manager_info,
            role=manager_role
        )

        pay = PayCheck(
            emp_role=manager
        )
        time = TimeCard(
            paycheck=pay
        )
        entry = Entry(
            hour_type=HourType.REGULAR,
            hours=8,
            timecard=time
        )


        self.this_session.add_all(
            (manager_role, manager_info, manager, pay, time, entry)
        )
        self.this_session.flush()

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
            supplier_id=supplier,
            branch_id=branch
        )
        self.this_session.add(new_invoice)

        out_invoice = self.this_session.query(Invoice).filter_by(invoice_id=1).first()
        self.assertEqual(out_invoice.supplier_id, supplier)
        self.assertEqual(out_invoice.branch_id, branch)

if __name__ == '__main__':
    unittest.main()
