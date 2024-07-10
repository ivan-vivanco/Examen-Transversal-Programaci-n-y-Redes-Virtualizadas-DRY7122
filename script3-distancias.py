import requests
from math import radians, cos, sin, sqrt, atan2

def obtener_coordenadas(mendoza):
    url = f"https://nominatim.openstreetmap.org/search?q={mendoza}&format=json&addressdetails=1"
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  
        datos = respuesta.json()
        if datos:
            return datos[0]['lat'], datos[0]['lon']
        else:
            print(f"No se encontraron coordenadas para la ciudad: {ciudad}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP: {e}")
        return None, None
    except ValueError:
        print(f"Respuesta JSON inválida para la ciudad: {ciudad}")
        return None, None

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0  

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia_km = R * c
    distancia_millas = distancia_km * 0.621371
    return distancia_km, distancia_millas

def calcular_duracion(distancia, medio_transporte):
    velocidades = {
        'auto': 80,  # km/h
        'bus': 60,   # km/h
        'tren': 100, # km/h
        'avion': 900 # km/h
    }
    if medio_transporte in velocidades:
        duracion_horas = distancia / velocidades[medio_transporte]
        return duracion_horas
    else:
        return None

def mostrar_narrativa(ciudad_origen, ciudad_destino, distancia_km, distancia_millas, duracion_horas, medio_transporte):
    print(f"De {ciudad_origen} a {ciudad_destino}:")
    print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
    print(f"Duración estimada del viaje en {medio_transporte}: {duracion_horas:.2f} horas")

def main():
    while True:
        ciudad_origen = input("Ingrese Ciudad de Origen: ")
        if ciudad_origen.lower() == 's':
            break
        ciudad_destino = input("Ingrese Ciudad de Destino: ")
        if ciudad_destino.lower() == 's':
            break

        lat1, lon1 = obtener_coordenadas(ciudad_origen)
        lat2, lon2 = obtener_coordenadas(ciudad_destino)

        if lat1 and lon1 and lat2 and lon2:
            distancia_km, distancia_millas = calcular_distancia(float(lat1), float(lon1), float(lat2), float(lon2))

            print("Elija el medio de transporte (auto, bus, tren, avion): ")
            medio_transporte = input().lower()

            duracion_horas = calcular_duracion(distancia_km, medio_transporte)

            if duracion_horas is not None:
                mostrar_narrativa(ciudad_origen, ciudad_destino, distancia_km, distancia_millas, duracion_horas, medio_transporte)
            else:
                print("Medio de transporte no válido. Intente de nuevo.")
        else:
            print("No se pudo obtener las coordenadas de una de las ciudades. Intente de nuevo.")

if __name__ == "__main__":
    main()
