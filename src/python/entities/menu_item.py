from sqlalchemy import *
from sqlalchemy.orm import relationship
from entities import Base

class MenuItem(Base):
    __tablename__= 'menuItem'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    price = Column(Float(precision='7,2'), nullable=False)

    UniqueConstraint(name)

    def __repr__(self):
        return (
            'MenuItem(id={}, name={}, type={}, price={})'
        ).format(
            self.id,
            self.name,
            self.type,
            self.price
        )
