import requests
import base64
import json

# Tus credenciales
client_id = ''
client_secret = ''

# Codifica las credenciales en base64
auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

# URL para obtener el token
token_url = 'https://accounts.spotify.com/api/token'

# Datos y encabezados para la solicitud del token
token_data = {
    'grant_type': 'client_credentials'
}

token_headers = {
    'Authorization': f'Basic {b64_auth_str}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Solicitud POST para obtener el token
token_response = requests.post(token_url, headers=token_headers, data=token_data)
token_response_data = token_response.json()

# Extrae el token de acceso
access_token = token_response_data['access_token']

# Función para obtener el ID del artista a partir de su nombre
def get_artist_id(artist_name, access_token):
    search_url = 'https://api.spotify.com/v1/search'
    search_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    search_params = {
        'q': artist_name,
        'type': 'artist',
        'limit': 1
    }
    search_response = requests.get(search_url, headers=search_headers, params=search_params)
    search_data = search_response.json()
    return search_data['artists']['items'][0]['id']

# Solicitar el nombre del artista al usuario
artist_name = input("Ingresa el nombre del artista: ")

# Obtener el ID del artista
artist_id = get_artist_id(artist_name, access_token)

# URL para obtener la información del artista
artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'

# Encabezados para la solicitud GET
artist_headers = {
    'Authorization': f'Bearer {access_token}'
}

# Solicitud GET para obtener la información del artista
artist_response = requests.get(artist_url, headers=artist_headers)
artist_data = artist_response.json()

# Guardar la información del artista en un archivo JSON
filename = f"{artist_name.replace(' ', '_')}_info.json"
with open(filename, 'w') as f:
    json.dump(artist_data, f, indent=4)

print(f"La información del artista se ha guardado en el archivo {filename}")

# Imprime la información del artista
print(f"Name: {artist_data['name']}")
print(f"Followers: {artist_data['followers']['total']}")
print(f"Genres: {', '.join(artist_data['genres'])}")
print(f"Popularity: {artist_data['popularity']}")
print(f"Spotify URL: {artist_data['external_urls']['spotify']}")

# Imprime las imágenes del artista
for image in artist_data['images']:
    print(f"Image URL ({image['height']}x{image['width']}): {image['url']}")
