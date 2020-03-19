from sqlalchemy.ext.declarative import declarative_base 

import enum

Base = declarative_base()

class TableNames(enum.Enum):
    LINE_ITEM = 'lineItem'
    MENU_ITEM = 'menuItem'
    RECEIPT = 'receipt'
