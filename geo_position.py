# файл отвечает за распознование местоположения (в БД передает название города)
from geopy.geocoders import Nominatim
from db_postgreSQL import set_city_user_db


def set_city_geopy(user_id: int, latit:float, long:float) -> bool:
    geolocator = Nominatim(user_agent="SEA")
    location = geolocator.reverse(f"{latit}, {long}", language='ru')
    if location:
        loc_dict = location.raw
        city = loc_dict['address']['city'] + ', ' + loc_dict['address']['country']
        set_city_user_db(user_id=user_id, geopy_city=city)
        return True
    else:
        return False
