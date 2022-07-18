from .models import Customer
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save


def create_customer(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name="customer")
        instance.groups.add( group)
        username = instance.username
        name = instance.first_name
        last_name = instance.last_name
        email = instance.email
        fullname = f"{name} {last_name}"
        Customer.objects.create(user=instance, name=fullname,
                                username=username, phone=123456789,
                                email=email, )


post_save.connect(create_customer, sender=User)
