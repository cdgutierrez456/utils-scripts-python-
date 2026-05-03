import os
import sys
import ipinfo
import folium
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
IP_ADDRESS = "190.70.237.123"

def draw_map(latitude, longitude, location, filename="map.html"):
    """Dibuja un mapa basandose en los detalles de geolocalizacion de una IP"""
    my_map = folium.Map(location=[latitude, longitude], zoom_start=9)
    folium.Marker([latitude, longitude], popup=location).add_to(my_map)
    my_map.save(filename)
    return os.path.abspath(filename)

def get_ip_details(ip_addr, access_token):
    """Obtiene detalles de geolocalizacion de una IP utilizando ipinfo"""
    try:
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(ip_addr)
        return details.all
    except Exception as e:
        print(f"Error al obtener los detalles de la IP: {ip_addr}")
        sys.exit(1)


if __name__ == '__main__':
    details = get_ip_details(IP_ADDRESS, ACCESS_TOKEN)
    print(f'Detalles de la IP {IP_ADDRESS}:')

    # Mostramos los detalles de la IP por pantalla
    for key, value in details.items():
        print(f"{key}: {value}")

    # Obtenemos valores de latitud, longitud y ubicación para dibujar el mapa
    latitude = details['latitude']
    longitude = details['longitude']
    location = details.get('region', 'Unknown Location')

    # Dibujar el mapa
    map_file_path = draw_map(latitude, longitude, location)
    print(f'Mapa guardado en: {map_file_path}')