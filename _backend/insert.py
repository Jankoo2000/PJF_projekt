from datetime import datetime

from _backend import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()



def insertF(data):
    x = lambda f : 0 if(f[3].split(' ')[3] == "no") else int(f[3].split(' ')[3])
    y = lambda f : 0 if(f[7].split(' ')[3] == "no") else int(f[7].split(' ')[3])


    for flight in list(data):

        tr = db.Flights(
            date_dep_to_dest = flight[0],
            airport_dep_to_dest_place = ' '.join(flight[1].split(' ')[1:-1]),
            airport_dep_to_dest_code = flight[1].split(' ')[-1],
            hour_dep_to_dest = flight[1].split(' ')[0],
            date_arr_to_dest = flight[0],
            airport_arr_to_dest_place = ' '.join(flight[5].split(' ')[1:-1]),
            airport_arr_to_dest_code = flight[5].split(' ')[-1],
            hour_arr_to_dest = flight[2].split(' ')[0],
            flight_time_to_dest = flight[3].split(' ')[0],
            interchanges_to_dest = x(flight),

            date_dep_from = flight[4],
            airport_dep_from_place = ' '.join(flight[5].split(' ')[1:-1]),
            airport_dep_from_code = flight[5].split(' ')[-1],
            hour_dep_from = flight[5].split(' ')[0],
            date_arr_from = flight[4],
            airport_arr_from_place = ' '.join(flight[1].split(' ')[1:-1]),
            airport_arr_from_code = flight[1].split(' ')[-1],
            hour_arr_from = flight[6].split(' ')[0],
            flight_time_from = flight[7].split(' ')[0],
            interchanges_from = y(flight),
            total_prize = int(flight[8].split(' ')[0]),
            days = int(abs((flight[0] - flight[4]).days)),
            url = flight[9]
        )
        session.add(tr)

    session.commit()

