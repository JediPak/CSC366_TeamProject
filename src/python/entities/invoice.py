import datetime

from sqlalchemy import *
from entities import Base

class Invoice(Base):
    __tablename__ = 'invoice'

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier = Column(Integer, ForeignKey('supplier.supplier_id'), nullable=False)
    date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    branch = Column(Integer, ForeignKey('store.store_id'), nullable=False)

    def __repr__(self):
        return "Invoice(id={}, supplier={}, date={}, branch={})".format(
            self.invoice_id,
            self.supplier,
            self.date,
            self.branch
        )
