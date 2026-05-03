import os
import folium
import phonenumbers
from geopy.geocoders import Photon
from phonenumbers import geocoder, carrier, timezone
from dotenv import load_dotenv

def get_info_phone(number_phone):
    """Obtener datso de geolozalizacion de un numer de telefono"""
    number = phonenumbers.parse(number_phone)

    # Get timezone
    time_zone = timezone.time_zones_for_number(number)

    # Get country
    country = geocoder.description_for_number(number, 'en')

    # Get number operator
    operator = carrier.name_for_number(number, 'en')

    info = {
        "Numero": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "Pais": country,
        "Operador": operator,
        "Zona Horaria": time_zone
    }

    return info

def print_map(localization, filename="phone_map.html"):
    """Construye un mapa con la localizacion de un numero de telefono"""
    geolocator = Photon(user_agent="geoapiExcercise")
    location = geolocator.geocode(localization)
    map = folium.Map(location=[location.latitude, location.longitude], zoom_start=10)
    folium.Marker([location.latitude, location.longitude], popup=localization).add_to(map)

    # Save map in html file
    map.save(filename)
    print(f'Mapa guardado en: {filename}')

if __name__ == '__main__':
    load_dotenv()
    number_phone = os.getenv('PHONE_NUMBER')
    info = get_info_phone(number_phone)

    print_map(info['Pais'])
    print(f'Info de telefono {info}:')