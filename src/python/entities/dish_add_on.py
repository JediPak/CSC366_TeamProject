from sqlalchemy import Column, Integer, String, ForeignKey

from entities import Base, TableNames

class DishAddOn(Base):
    __tablename__ = TableNames.DISH_ADD_ON.value

    main_dish_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.MAIN_DISH.value),default=None), primary_key=True)
    add_on_id = Column(Integer, ForeignKey('{}.id'.format(TableNames.ADD_ON.value),default=None), primary_key=True)


    def __repr__(self):
        return "DishAddOn(main_dish_id={}, add_on_id={})".format(
            self.main_dish_id,
            self.add_on_id
        )
