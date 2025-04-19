# Guía de Instalación y Configuración

Esta guía te ayudará a configurar correctamente el entorno para ejecutar los scripts de transferencia de Spotify a YouTube Music.

## 1. Preparación del entorno

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Acceso a internet
- Cuentas en Spotify y YouTube Music

### Configuración del entorno virtual

Es recomendable utilizar un entorno virtual para aislar las dependencias del proyecto:

```bash
# Clonar el repositorio (si aún no lo has hecho)
git clone https://github.com/tu-usuario/spotify-to-ytmusic-transfer.git
cd spotify-to-ytmusic-transfer

# Crear el entorno virtual
python -m venv env

# Activar el entorno virtual
# En Linux/Mac:
source env/bin/activate
# En Windows:
env\Scripts\activate

# Instalar las dependencias
pip install -r requirements.txt
```

## 2. Configuración de las APIs

### 2.1 Configurar la API de Spotify

1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Inicia sesión con tu cuenta de Spotify
3. Haz clic en "Create an App"
4. Completa los detalles de la aplicación:
   - Nombre: "Spotify to YT Music Transfer" (o el que prefieras)
   - Descripción: "Aplicación para transferir contenido de Spotify a YouTube Music"
5. Acepta los términos y condiciones
6. Una vez creada, anota el **Client ID** y el **Client Secret**
7. Haz clic en "Edit Settings" y agrega `http://127.0.0.1:8888/callback` como URI de redirección
8. Guarda los cambios

### 2.2 Configurar la autenticación de YouTube Music

Ejecuta el script de configuración:

```bash
python setup_ytmusic.py
```

Sigue las instrucciones en pantalla:
1. Abre YouTube Music en tu navegador
2. Inicia sesión en tu cuenta
3. Abre las herramientas de desarrollador (F12 o Ctrl+Shift+I)
4. Ve a la pestaña "Network"
5. Recarga la página (F5)
6. Busca cualquier petición a "music.youtube.com"
7. Haz clic derecho en la petición y selecciona "Copy as cURL" (en Chrome) o "Copy Request Headers" (en Firefox)
8. Pega el contenido en la terminal cuando el script te lo pida

Esto creará un archivo `headers_auth.json` que contiene tu información de autenticación.

## 3. Modificación de los scripts

Edita los scripts `spotify_to_ytmusic.py` y/o `spotify_to_ytmusic_playlists.py` para agregar tus credenciales de Spotify:

```python
# Configuración de Spotify
SPOTIPY_CLIENT_ID = 'tu_client_id_aquí'
SPOTIPY_CLIENT_SECRET = 'tu_client_secret_aquí'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'
```

## 4. Verificación

Antes de ejecutar los scripts principales, puedes verificar que la conexión con YouTube Music funciona correctamente:

```bash
python test_ytmusic.py
```

Si todo está configurado correctamente, deberías ver resultados de búsqueda de YouTube Music.

## 5. Ejecución

Ahora puedes ejecutar los scripts principales:

```bash
# Para transferir canciones favoritas
python spotify_to_ytmusic.py
```

## Solución de problemas

- **Error de autenticación con Spotify**: Verifica que las credenciales y la URI de redirección sean correctas.
- **Error con YouTube Music**: Regenera el archivo headers_auth.json siguiendo los pasos de la sección 2.2.
- **Límites de tasa**: Si recibes errores relacionados con límites de tasa, modifica los tiempos de espera en los scripts para hacerlos más largos.
