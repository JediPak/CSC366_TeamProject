import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from entities import Base, TableNames

class Invoice(Base):
    __tablename__ = TableNames.INVOICE.value

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('supplier.supplier_id'), nullable=False)
    supplier = relationship("Supplier")
    date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    branch_id = Column(Integer, ForeignKey('branch.id'), nullable=False)
    branch = relationship("Branch")


    def __repr__(self):
        return "Invoice(id={}, supplier={}, date={}, branch={})".format(
            self.invoice_id,
            self.supplier_id,
            self.date,
            self.branch_id
        )
