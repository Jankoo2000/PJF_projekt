from sqlalchemy import create_engine, Column, Integer, String, Identity, DATE, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///flight.db", echo=True)

base = declarative_base()


class Flights(base):
    __tablename__ = "flights"

    id = Column(Integer,Identity(start=0, cycle=True), primary_key=True)
    date_dep_to_dest = Column(DATE)
    airport_dep_to_dest_place = Column(String)
    airport_dep_to_dest_code = Column(String)
    hour_dep_to_dest = Column(String)
    date_arr_to_dest = Column(DATE)
    airport_arr_to_dest_place = Column(String)
    airport_arr_to_dest_code = Column(String)
    hour_arr_to_dest = Column(String)
    flight_time_to_dest = Column(String)
    interchanges_to_dest = Column(Integer)
    date_dep_from = Column(DATE)
    airport_dep_from_place = Column(String)
    airport_dep_from_code = Column(String)
    hour_dep_from = Column(String)
    date_arr_from = Column(DATE)
    airport_arr_from_place = Column(String)
    airport_arr_from_code = Column(String)
    hour_arr_from = Column(String)
    flight_time_from = Column(String)
    interchanges_from = Column(Integer)
    total_prize = Column(Integer)
    days = Column(Integer)
    url = Column(String)



base.metadata.create_all(engine)


