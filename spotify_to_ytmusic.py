import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import time
import json
import os
from datetime import datetime

# Configuración de Spotify
SPOTIPY_CLIENT_ID = 'TU_CLIENT_ID_AQUÍ'
SPOTIPY_CLIENT_SECRET = 'TU_CLIENT_SECRET_AQUÍ'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'
scope = "user-library-read playlist-read-private playlist-read-collaborative"

# Crear directorio para logs y respaldos
os.makedirs('logs', exist_ok=True)
os.makedirs('backups', exist_ok=True)

# Función para formatear nombre de archivo con timestamp
def get_timestamp_filename(prefix, ext='json'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{ext}"

# Iniciar sesión en Spotify
print("Iniciando sesión en Spotify...")
auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
)

# Obtén el token manualmente
auth_url = auth_manager.get_authorize_url()
print(f'Por favor, visita esta URL en tu navegador: {auth_url}')
redirect_url = input('Ingresa la URL completa a la que fuiste redirigido: ')
code = auth_manager.parse_response_code(redirect_url)
token = auth_manager.get_access_token(code, as_dict=False)

# Crear cliente de Spotify con el token
sp = spotipy.Spotify(auth=token)

# Conectar a YouTube Music
print("Conectando a YouTube Music...")
try:
    ytmusic = YTMusic('headers_auth.json')
    print("Conexión exitosa con YouTube Music")
except Exception as e:
    print(f"Error al conectar con YouTube Music: {e}")
    print("Por favor, regenera el archivo headers_auth.json")
    exit(1)

# Obtener playlists de Spotify
def get_spotify_playlists():
    print("Obteniendo tus playlists de Spotify...")
    playlists = []
    results = sp.current_user_playlists()
    
    while results:
        for item in results['items']:
            # Solo incluir playlists creadas por el usuario o colaborativas
            if item['owner']['id'] == sp.me()['id'] or item.get('collaborative', False):
                playlist_id = item['id']
                playlist_name = item['name']
                playlist_desc = item.get('description', '')
                playlists.append({
                    'id': playlist_id,
                    'name': playlist_name,
                    'description': playlist_desc,
                    'tracks': []
                })
        
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    print(f"Se encontraron {len(playlists)} playlists.")
    return playlists

# Obtener canciones de una playlist de Spotify
def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id)
    
    while results:
        for item in results['items']:
            if item['track']:  # Verificar que la pista existe
                track = item['track']
                name = track['name']
                artists = [artist['name'] for artist in track['artists']]
                artist_str = ', '.join(artists)
                album = track.get('album', {}).get('name', '')
                tracks.append({
                    'name': name, 
                    'artist': artist_str,
                    'album': album
                })
        
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return tracks

# Buscar canción en YouTube Music
def search_song_in_ytmusic(track):
    query = f"{track['name']} {track['artist']}"
    try:
        search_results = ytmusic.search(query)
        song_results = [item for item in search_results if item.get('resultType') == 'song']
        
        if song_results:
            return song_results[0]['videoId']
        else:
            # Intento alternativo solo con el título
            search_results = ytmusic.search(track['name'])
            song_results = [item for item in search_results if item.get('resultType') == 'song']
            
            if song_results:
                return song_results[0]['videoId']
            
    except Exception as e:
        print(f"Error buscando {query}: {e}")
    
    return None

# Crear playlist en YouTube Music
def create_ytmusic_playlist(playlist_name, playlist_desc):
    try:
        playlist_id = ytmusic.create_playlist(
            title=playlist_name,
            description=playlist_desc
        )
        return playlist_id
    except Exception as e:
        print(f"Error creando playlist: {e}")
        return None

# Transferir playlists de Spotify a YouTube Music
def transfer_playlists():
    # Obtener playlists de Spotify
    spotify_playlists = get_spotify_playlists()
    
    # Guardar backup de las playlists
    backup_filename = f"backups/{get_timestamp_filename('spotify_playlists')}"
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(spotify_playlists, f, ensure_ascii=False, indent=4)
    print(f"Respaldo de playlists guardado en {backup_filename}")
    
    # Preguntar al usuario qué playlists transferir
    print("\nPlaylists disponibles:")
    for i, playlist in enumerate(spotify_playlists):
        print(f"{i+1}. {playlist['name']} ({len(get_playlist_tracks(playlist['id']))} canciones)")
    
    playlist_indices = input("\nIngresa los números de las playlists a transferir (separados por coma) o 'all' para todas: ")
    
    if playlist_indices.lower() == 'all':
        playlists_to_transfer = spotify_playlists
    else:
        indices = [int(idx.strip()) - 1 for idx in playlist_indices.split(',')]
        playlists_to_transfer = [spotify_playlists[i] for i in indices if 0 <= i < len(spotify_playlists)]
    
    # Resultados y estadísticas
    transfer_results = []
    
    # Procesar cada playlist
    for playlist in playlists_to_transfer:
        print(f"\nProcesando playlist: {playlist['name']}")
        
        # Obtener todas las canciones de la playlist
        print("Obteniendo canciones...")
        tracks = get_playlist_tracks(playlist['id'])
        playlist['tracks'] = tracks
        print(f"Se encontraron {len(tracks)} canciones en esta playlist")
        
        # Crear la playlist en YouTube Music
        print(f"Creando playlist '{playlist['name']}' en YouTube Music...")
        ytmusic_playlist_id = create_ytmusic_playlist(playlist['name'], playlist['description'])
        
        if not ytmusic_playlist_id:
            print("No se pudo crear la playlist en YouTube Music. Continuando con la siguiente...")
            transfer_results.append({
                'playlist': playlist['name'],
                'status': 'error',
                'tracks_found': 0,
                'tracks_not_found': 0
            })
            continue
        
        print(f"Playlist creada con ID: {ytmusic_playlist_id}")
        
        # Buscar y añadir canciones
        found_tracks = []
        not_found_tracks = []
        
        for i, track in enumerate(tracks):
            print(f"[{i+1}/{len(tracks)}] Buscando: {track['name']} - {track['artist']}")
            
            video_id = search_song_in_ytmusic(track)
            
            if video_id:
                found_tracks.append({**track, 'videoId': video_id})
                # Añadir a la playlist
                try:
                    ytmusic.add_playlist_items(ytmusic_playlist_id, [video_id])
                    print(f"✅ Añadida a la playlist: {track['name']} - {track['artist']}")
                except Exception as e:
                    print(f"❌ Error añadiendo a playlist: {e}")
            else:
                not_found_tracks.append(track)
                print(f"❌ No se encontró: {track['name']} - {track['artist']}")
            
            # Pausa para evitar límites de tasa
            if (i + 1) % 5 == 0:
                print("Esperando 5 segundos...")
                time.sleep(5)
            else:
                time.sleep(1.5)
        
        # Guardar resultados
        transfer_results.append({
            'playlist': playlist['name'],
            'status': 'success',
            'youtube_playlist_id': ytmusic_playlist_id,
            'tracks_found': len(found_tracks),
            'tracks_not_found': len(not_found_tracks),
            'not_found_tracks': not_found_tracks
        })
        
        print(f"\nResumen de la playlist '{playlist['name']}':")
        print(f"- Total de canciones: {len(tracks)}")
        print(f"- Canciones encontradas y añadidas: {len(found_tracks)}")
        print(f"- Canciones no encontradas: {len(not_found_tracks)}")
    
    # Guardar log de resultados
    log_filename = f"logs/{get_timestamp_filename('transfer_log')}"
    with open(log_filename, 'w', encoding='utf-8') as f:
        json.dump(transfer_results, f, ensure_ascii=False, indent=4)
    
    print(f"\nTransferencia completada. Log guardado en {log_filename}")
    
    # Mostrar resumen general
    total_playlists = len(playlists_to_transfer)
    successful_playlists = sum(1 for r in transfer_results if r['status'] == 'success')
    failed_playlists = total_playlists - successful_playlists
    
    total_tracks = sum(len(p['tracks']) for p in playlists_to_transfer)
    total_found = sum(r['tracks_found'] for r in transfer_results)
    total_not_found = sum(r['tracks_not_found'] for r in transfer_results)
    
    print("\n==== RESUMEN FINAL ====")
    print(f"Playlists procesadas: {successful_playlists}/{total_playlists}")
    print(f"Canciones procesadas: {total_tracks}")
    print(f"Canciones encontradas y añadidas: {total_found} ({(total_found/total_tracks*100):.1f}%)")
    print(f"Canciones no encontradas: {total_not_found} ({(total_not_found/total_tracks*100):.1f}%)")

# Ejecutar la transferencia de playlists
if __name__ == "__main__":
    # Menú principal
    print("\n==== SPOTIFY A YOUTUBE MUSIC ====")
    print("1. Transferir playlists")
    print("2. Transferir canciones favoritas (Me gusta)")
    
    option = input("Selecciona una opción (1-2): ")
    
    if option == "1":
        transfer_playlists()
    elif option == "2":
        # Aquí puedes llamar a la función para transferir los Me gusta
        # Esta sería la funcionalidad de tu script original
        print("Esta funcionalidad no está implementada en este script.")
        print("Usa spotify_to_ytmusic.py para transferir tus canciones favoritas.")
    else:
        print("Opción no válida.")
