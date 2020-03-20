from sqlalchemy import *
from sqlalchemy.orm import relationship
from entities import Base, TableNames

class InvoiceItem(Base):
    __tablename__ = TableNames.INVOICE_ITEM.value

    invoice_id = Column(Integer, ForeignKey('invoice.invoice_id'), primary_key=True)
    invoice = relationship("Invoice")
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    quantity = Column(Integer, CheckConstraint('quantity > 0'), nullable=False)
    price = Column(Float(precision='5,2'))

    def __repr__(self):
        return "InvoiceItem(invoice={}, item={}, qty={}, price={})".format(
            self.invoice_id,
            self.item_id,
            self.quantity,
            self.price
        )
