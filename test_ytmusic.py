from ytmusicapi import YTMusic
import json

try:
    print("Intentando conectar con YouTube Music...")
    ytmusic = YTMusic('headers_auth.json')
    
    # Prueba una búsqueda simple
    print("Realizando búsqueda de prueba...")
    results = ytmusic.search("Bad Bunny", limit=1)
    
    print("\nResultados de la búsqueda:")
    print(json.dumps(results, indent=2))
    
    print("\n¡Conexión exitosa con YouTube Music!")
except Exception as e:
    print(f"Error al conectar: {e}")
