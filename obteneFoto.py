import requests
import random


def get_random_person_image():
    # Reemplaza 'TU_API_KEY' con tu clave de acceso a la API de Unsplash
    api_key = 'WuFMTvB9iHnH8JsX9wdxvvl-eFG1rVD2HyBjY_-3bDY'

    # URL de la API de búsqueda de Unsplash para obtener imágenes de personas
    url = 'https://api.unsplash.com/search/photos'

    # Parámetros de la solicitud
    params = {
        'query': 'person',
        'per_page': 30,
        'client_id': api_key
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Obtener una imagen aleatoria de persona de los resultados
            results = data.get('results', [])
            if results:
                random_image = random.choice(results)
                image_url = random_image['urls']['regular']
                return image_url
        else:
            print("Error al obtener la imagen:", data.get('errors', ''))
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)

    return None


# Obtener una URL de imagen de persona aleatoria
avatar_url = get_random_person_image()
print(avatar_url)
