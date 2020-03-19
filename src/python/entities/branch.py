from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from entities import Base, TableNames

class Branch(Base):
    __tablename__ = TableNames.BRANCH.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(Integer, nullable=False)

    manager_id = Column(
        Integer, 
        ForeignKey('{}.id'.format(TableNames.EMPLOYEE.value)),
        nullable=False
    )

    manager = relationship('Employee', foreign_keys=[manager_id])

    def __repr__(self):
        return 'Store(id={}, address={}, city={}, state={}, zip_code={})'.format(
            self.store_id,
            self.address,
            self.city,
            self.state,
            self.zip_code
        )
