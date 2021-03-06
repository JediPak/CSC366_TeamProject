from sqlalchemy import *
from sqlalchemy.orm import relationship

from entities import Base, TableNames
class Supplier(Base):
    __tablename__ = TableNames.SUPPLIER.value

    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(Integer, nullable=False)

    def __repr__(self):
        return "Supplier(id={}, address={}, city={}, state={}, zip={})".format(
            self.supplier_id,
            self.address,
            self.city,
            self.state,
            self.zip_code
        )
