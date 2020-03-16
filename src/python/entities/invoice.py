from sqlalchemy import Column, Integer, String, DateTime

from entities import Base

class Invoice(Base):
    __tablename__ = 'store'

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier = Column(Integer, nullable=False)
    date = Column(Datetime, nullable=False)
    branch = Column(Integer, nullable=False)

    def __repr__(self):
        return "Invoice(id={}, supplier={}, date={}, branch={})".format(
            self.invoice_id,
            self.supplier,
            self.date,
            self.branch
        )
