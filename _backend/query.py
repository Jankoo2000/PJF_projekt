from datetime import datetime
from sqlalchemy import func
from _backend import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()


def id_return_flight(flight):
    x = lambda f : 0 if(f[3].split(' ')[3] == "no") else int(f[3].split(' ')[3])
    y = lambda f : 0 if(f[7].split(' ')[3] == "no") else int(f[7].split(' ')[3])

    result = session.query(db.Flights).filter(
        db.Flights.date_dep_to_dest == flight[0].split(' ')[1],
        db.Flights.airport_dep_to_dest == flight[1].split(' ')[1] + " " + flight[1].split(' ')[2],
        db.Flights.hour_dep_to_dest == flight[1].split(' ')[0],
        db.Flights.date_arr_to_dest == flight[0].split(' ')[1],
        db.Flights.airport_arr_to_dest == flight[2].split(' ')[1] + " " + flight[2].split(' ')[2],
        db.Flights.hour_arr_to_dest == flight[2].split(' ')[0],
        db.Flights.flight_time_to_dest == flight[3].split(' ')[0],
        db.Flights.interchanges_to_dest == x(flight),
        db.Flights.date_dep_from == flight[4].split(' ')[1],
        db.Flights.airport_dep_from == flight[5].split(' ')[1] + " " + flight[5].split(' ')[2],
        db.Flights.hour_dep_from == flight[5].split(' ')[0],
        db.Flights.date_arr_from == flight[4].split(' ')[1],
        db.Flights.airport_arr_from == flight[6].split(' ')[1] + " " + flight[6].split(' ')[2],
        db.Flights.hour_arr_from == flight[6].split(' ')[0],
        db.Flights.flight_time_from == flight[7].split(' ')[0],
        db.Flights.interchanges_from == y(flight),
        db.Flights.total_prize == int(flight[8].split(' ')[0])
    )



def complicant_data_to_file(dane):


    result = session.query(
                        db.Flights.date_dep_to_dest,
                        db.Flights.airport_dep_to_dest_place,
                        db.Flights.airport_dep_to_dest_code,
                        db.Flights.hour_dep_to_dest,
                        db.Flights.date_arr_to_dest ,
                        db.Flights.airport_arr_to_dest_place,
                        db.Flights.airport_arr_to_dest_code ,
                        db.Flights.hour_arr_to_dest ,
                        db.Flights.flight_time_to_dest ,
                        db.Flights.interchanges_to_dest ,

                        db.Flights.date_dep_from ,
                        db.Flights.airport_dep_from_place,
                        db.Flights.airport_dep_from_code ,
                        db.Flights.hour_dep_from ,
                        db.Flights.date_arr_from ,
                        db.Flights.airport_arr_from_place ,
                        db.Flights.airport_arr_from_code ,
                        db.Flights.hour_arr_from ,
                        db.Flights.flight_time_from ,
                        db.Flights.interchanges_from ,
                        db.Flights.total_prize ,
                        db.Flights.url

                    ).filter(

                        db.Flights.airport_dep_to_dest_code.in_(dane[8]),
                        db.Flights.airport_dep_from_code.in_(dane[9]),
                        db.Flights.date_dep_to_dest >= datetime.strptime(dane[3], "%Y-%m-%d"),
                        db.Flights.date_arr_from <= datetime.strptime(dane[4], "%Y-%m-%d"),
                        db.Flights.total_prize <= int(dane[7]),
                        db.Flights.days >= int(dane[5]),
                        db.Flights.days <= int(dane[6])

                    ).order_by(
                        db.Flights.total_prize
                    ).\
                    distinct()


    if(result.count() !=0):
        file = open("flights.txt", "w")
        for f in result:
                file.write(

                    str(f.date_dep_to_dest) + " | " +
                    f.airport_dep_to_dest_place + "  " +
                    f.airport_dep_to_dest_code + " -> " +
                    f.airport_arr_to_dest_place + "  " +
                    f.airport_arr_to_dest_code + " ||| " +

                    str(f.date_dep_from) + " | " +
                    f.airport_dep_from_place + " | " +
                    f.airport_dep_from_code + " -> " +
                    f.airport_arr_from_place + "  " +
                    f.airport_arr_from_code + " | " +
                    str(f.total_prize) + " \n" +
                    f.url + "\n\n"
                )
        file.close()


def delete_old_rows():
    result = session.query(db.Flights).filter(
        db.Flights.date_dep_to_dest < func.now()
    )
    print(result.count())
    result.delete(synchronize_session=False)
    session.commit()


