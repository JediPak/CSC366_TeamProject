import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from entities import Base

class Invoice(Base):
    __tablename__ = 'invoice'

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('supplier.supplier_id'), nullable=False)
    supplier = relationship("Supplier")
    date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    store_id = Column(Integer, ForeignKey('store.store_id'), nullable=False)
    store = relationship("Store")


    def __repr__(self):
        return "Invoice(id={}, supplier={}, date={}, branch={})".format(
            self.invoice_id,
            self.supplier,
            self.date,
            self.store_id
        )
