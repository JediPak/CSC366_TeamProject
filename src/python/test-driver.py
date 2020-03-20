import unittest

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from entities import Base
from entities.branch import Branch
from entities.employee import *
from entities.pay import PayCheck, TimeCard, Entry, HourType
from entities.order import *


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


    def test_add_food_items(self):
        cilantro = Ingredient(
            name = "Cilantro"
        )

        fish = Ingredient(
            name = "Fish"
        )

        lemon = Ingredient(
            name = "Lemon"
        )

        add_on = AddOn(
            name = "Sour Cream",
            type = ItemType.ADDON,
            price = 0.75
        )

        main_dish = MainDish(
            name = "Ceviche",
            type = ItemType.APPETIZER,
            price = 12.50,
        )
        main_dish.ingredients.append(fish)
        main_dish.ingredients.append(cilantro)
        main_dish.ingredients.append(lemon)

        premade_item = PremadeItem(
            name = "Housemade Tortilla Chips",
            type = ItemType.PREMADE,
            price = 3.00,
            sell_by = datetime.date(2020, 3, 24),
            packaged_on = datetime.date(2020, 3, 19)
        )

        self.this_session.add_all(
            (cilantro,
            fish,
            lemon,
            add_on, 
            main_dish, 
            premade_item)
        )

        self.this_session.flush()


if __name__ == '__main__':
    unittest.main()