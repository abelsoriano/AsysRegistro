from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CambioDirectiva, Miembro, Cargo

@receiver(post_save, sender=CambioDirectiva)
def update_miembros_cargo(sender, instance, **kwargs):
    cargos = {
        'presidente': instance.presidente,
        'vicepresidente': instance.vicepresidente,
        'secretario': instance.secretario,
        'sub_secretario': instance.sub_secretario,
        'tesorero': instance.tesorero,
        'primer_vocal': instance.primer_vocal,
    }

    try:
        cargo_miembro_default = Cargo.objects.get(name="Miembro")
    except Cargo.DoesNotExist:
        print("El cargo 'Miembro' no existe en la base de datos.")
        return

    for cargo_name, miembro in cargos.items():
        if miembro:
            cargo = Cargo.objects.get(name=cargo_name.capitalize())

            # Ensure no other member in the same category has this role
            Miembro.objects.filter(cargo=cargo, category=miembro.category).update(cargo=cargo_miembro_default)

            # Assign the new role to the current member
            miembro.cargo = cargo
            miembro.save()

    # Update roles for outgoing members to "Miembro"
    miembros_salientes = Miembro.objects.filter(cargo__name__in=cargos.keys()).exclude(
        id__in=[miembro.id for miembro in cargos.values() if miembro is not None])

    for miembro in miembros_salientes:
        miembro.cargo = cargo_miembro_default
        miembro.save()
