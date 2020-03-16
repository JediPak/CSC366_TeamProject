from sqlalchemy import Column, Integer, String

from entities import Base

class InvoiceItem(Base):
    __tablename__ = 'store'

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float(precision='5,2'))
    CheckConstraint('quantity > 0')

    def __repr__(self):
        return "InvoiceItem(invoice={}, item={}, qty={}, price={})".format(
            self.invoice_id,
            self.item_id,
            self.quantity,
            self.price
        )
