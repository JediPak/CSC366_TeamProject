from sqlalchemy import Column, Integer, String

from entities import Base

class Store(Base):
    __tablename__ = 'store'

    store_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(Integer, nullable=False)

    def __repr__(self):
        return "Store(id={}, address={}, city={}, state={}, zip={})".format(
            self.store_id,
            self.address,
            self.city,
            self.state,
            self.zip_code
        )
