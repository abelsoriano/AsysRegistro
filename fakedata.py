from faker import Faker
import random

fake = Faker()


def generar_persona():
    gender_choices = ['masculino', 'femenino']
    estado_choices = ['Activo', 'Inactivo']

    persona = {
        'name': fake.first_name(),
        'lastname': fake.last_name(),
        'dni': fake.random_number(digits=11),
        'gender': random.choice(gender_choices),
        'date_joined': fake.date_of_birth().strftime('%d/%m/%Y'),
        'address': fake.address(),
        'fecha_ingreso': fake.future_date(end_date='+30d').strftime('%d/%m/%Y'),
        'phone': fake.phone_number(),
        'email': fake.email(),
        'cargo': 'Miembro',
        'avatar': fake.image_url(),
        'state': random.choice(estado_choices)
    }

    return persona


if __name__ == '__main__':
    for _ in range(20):  # Generar 10 personas aleatorias
        persona = generar_persona()
        print(persona)
