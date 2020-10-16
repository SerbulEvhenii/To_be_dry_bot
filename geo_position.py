from geopy.geocoders import Nominatim
from db_postgreSQL import set_city_user_db

def set_city_geopy(user_id, latit, long):
    geolocator = Nominatim(user_agent="SEA")
    location = geolocator.reverse(f"{latit}, {long}", language='ru')
    loc_dict = location.raw
    city = loc_dict['address']['city'] + ', ' + loc_dict['address']['country']
    set_city_user_db(user_id=user_id, geopy_city=city)




if __name__ == '__main__':
    print(city)
    print(loc_dict['address']['country'])
    print(loc_dict['address']['city'])
    print(location.address)

