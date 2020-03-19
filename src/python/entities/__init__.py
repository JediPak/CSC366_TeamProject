from sqlalchemy.ext.declarative import declarative_base

import enum

Base = declarative_base()

class TableNames(enum.Enum):
    ROLE = 'role'
    EMPLOYEE = 'employee'
    EMPLOYEE_INFO = 'employeeInfo'
    BRANCH = 'branch'
    PAYCHECK = 'paycheck'
    TIME_CARD = 'timeCard'
    TIME_CARD_ENTRY = 'timeCardEntry'
    LINE_ITEM = 'lineItem'
    MENU_ITEM = 'menuItem'
    RECEIPT = 'receipt'
    ADD_ON_INGREDIENT = 'addOnIngredient'
    ADD_ON = 'addOn'
    DISH_ADD_ON = 'dishAddOn'
    DISH_INGREDIENT = 'dishIngredient'
    INGREDIENT = 'ingredient'
    MAIN_DISH = 'mainDish'
    PREMADE_ITEM = 'premadeItem'
