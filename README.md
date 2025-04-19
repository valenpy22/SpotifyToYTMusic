# SpotifyToYTMusic

Herramienta para transferir contenido de Spotify a YouTube Music, incluyendo:
- Canciones favoritas (Me gusta)
- Playlists completas

## Descripción

Este proyecto proporciona una solución automatizada para migrar tu biblioteca musical de Spotify a YouTube Music. Utiliza las APIs oficiales de ambas plataformas para buscar y sincronizar tu contenido sin necesidad de servicios externos de pago.

## Características

- **Transferencia de "Me gusta"**: Sincroniza todas tus canciones favoritas de Spotify a YouTube Music
- **Transferencia de playlists**: Crea playlists en YouTube Music idénticas a las de Spotify
- **Interfaz sencilla**: Instrucciones paso a paso y menús interactivos
- **Respaldo automático**: Guarda copias de seguridad de tu biblioteca de Spotify
- **Registros detallados**: Genera informes sobre el proceso de transferencia

## Requisitos

- Python 3.8+
- Cuenta de Spotify
- Cuenta de YouTube Music
- Conexión a internet

## Instalación rápida

```bash
# Clonar el repositorio
git clone https://github.com/valenpy22/SpotifyToYTMusic.git
cd SpotifyToYTMusic

# Crear entorno virtual
python -m venv env

# Activar entorno
source env/bin/activate  # Linux/Mac
# o
env\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

Para instrucciones detalladas de instalación y configuración, consulta [INSTALL.md](INSTALL.md).

## Uso

### Transferir canciones favoritas y playlists

```bash
python spotify_to_ytmusic.py
```

El script te guiará a través del proceso de autenticación y selección de contenido a transferir.

## Scripts incluidos

- `setup_ytmusic.py`: Configura la autenticación con YouTube Music
- `test_ytmusic.py`: Verifica la conexión con YouTube Music
- `spotify_to_ytmusic.py`: Transfiere canciones favoritas o playlists completas

## Estructura del proyecto

```
SpotifyToYTMusic/
├── INSTALL.md              # Guía detallada de instalación
├── README.md               # Este archivo
├── requirements.txt        # Dependencias del proyecto
├── setup_ytmusic.py        # Script de configuración de YouTube Music
├── spotify_to_ytmusic.py   # Script para transferir favoritos o playlists
└── test_ytmusic.py         # Script de prueba de conexión
```

## Limitaciones

- La calidad de la transferencia depende de la disponibilidad de las canciones en YouTube Music
- Algunas canciones pueden no encontrarse exactamente debido a diferencias en los metadatos
- Las aplicaciones de desarrollador de Spotify tienen un límite de usuarios sin verificación

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request con tus mejoras.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
