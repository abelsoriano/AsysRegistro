import os
from django.core.files import File

import django

import random
import requests
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setting.settings")
django.setup()

from app.models import Miembro, Cargo, Estado

fake = Faker()

def get_random_person_image():
    # Reemplaza 'TU_API_KEY' con tu clave de acceso a la API de Unsplash
    api_key = 'WuFMTvB9iHnH8JsX9wdxvvl-eFG1rVD2HyBjY_-3bDY'

    # URL de la API de búsqueda de Unsplash para obtener imágenes de personas
    url = 'https://api.unsplash.com/search/photos'

    # Parámetros de la solicitud
    params = {
        'query': 'person',
        'per_page': 25,
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
# print(avatar_url)


def guardar_imagen(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)

def generate_phone_number():
    prefix = random.choice(['809', '829', '849'])
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return prefix + suffix
def generar_persona():
    gender_choices = ['Masculino', 'Femenino']
    estado_choices = ['Activo', 'Observacion']
    categori_choices = ['Dama', 'Caballero', 'Joven', 'Adolecente']
def generar_miembro():
    name = fake.first_name()
    lastname = fake.last_name()
    dni = fake.random_number(digits=11)
    gender_choices = [choice[0] for choice in Miembro._meta.get_field('gender').choices]
    gender = random.choice(gender_choices)
    date_joined = fake.date_of_birth().strftime('%Y-%m-%d')
    address = fake.address()
    fecha_ingreso = fake.future_date(end_date='+30d').strftime('%Y-%m-%d')
    phone = generate_phone_number()
    email = fake.email()
    cargo = random.choice(Cargo.objects.all())
    image = fake.image_url()
    state = random.choice(Estado.objects.all())
    categori_choices = [choice[0] for choice in Miembro._meta.get_field('category').choices]
    category = random.choice(categori_choices)

    avatar_url = get_random_person_image()
    image_filename = f'{name}_{lastname}.jpg'

    guardar_imagen(avatar_url, image_filename)
    miembro = Miembro.objects.get(pk=1)
    image_path = os.path.join('media', 'avatar', f'{name}_{lastname}.jpg')


    miembro = Miembro(
        name=name,
        lastname=lastname,
        dni=dni,
        gender=gender,
        date_joined=date_joined,
        address=address,
        fecha_ingreso=fecha_ingreso,
        phone=phone,
        email=email,
        cargo=cargo,
        # image = miembro.read_image(),
        state=state,
        category=category
    )
    with open(image_filename, "rb") as image_file:
        miembro.image.save(os.path.basename(image_path), File(image_file), save=True)
    miembro.save()

if __name__ == '__main__':
    for _ in range(20):  # Generar 10 miembros aleatorios con cargos aleatorios
        generar_miembro()
