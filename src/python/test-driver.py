import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities import Base
from entities.store import Store
from entities.employee import Employee, Role, Exemption, RoleName

from datetime import date

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

    def test2(self):
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

        manager_id = 1234
        manager_ssn = 555555555
        manager_name = 'Joe'
        start_date = date(1990, 1, 1)
        end_date = date(1990, 12, 31)
        manager_manager = None
        manager = Employee(
            emp_id=manager_id,
            ssn=manager_ssn,
            name=manager_name,
            start_date=start_date,
            end_date=end_date,
            manager=manager_manager,
            role=manager_role
        )

        managed_id = 12345
        managed_ssn = 444444444
        managed_name = 'Bill'
        managed = Employee(
            emp_id=managed_id,
            ssn=managed_ssn,
            name=managed_name,
            start_date=start_date,
            end_date=end_date,
            manager=manager,
            role=managed_role
        )
        self.this_session.add_all((manager_role, managed_role, manager, managed))

        out_emp = self.this_session.query(Employee).filter_by(ssn=managed_ssn).first()
        print(out_emp)
        self.assertEqual(out_emp.manager.emp_id, manager_id)

if __name__ == '__main__':
    unittest.main()