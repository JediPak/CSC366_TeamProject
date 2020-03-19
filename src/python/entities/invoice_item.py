from sqlalchemy import *

from entities import Base

class InvoiceItem(Base):
    __tablename__ = 'invoiceItem'

    invoice_id = Column(Integer, ForeignKey('invoice.invoice_id'), primary_key=True)
    item_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, CheckConstraint('quantity > 0'), nullable=False)
    price = Column(Float(precision='5,2'))

    def __repr__(self):
        return "InvoiceItem(invoice={}, item={}, qty={}, price={})".format(
            self.invoice_id,
            self.item_id,
            self.quantity,
            self.price
        )
