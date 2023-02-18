from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def add_superuser(apps, schema_editor=None):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    admin = User.objects.create(
        email="test_admin@admin.com",
        password=make_password("test_admin"),
        first_name="Migrated",
        last_name="Migrated Improved User",
        is_superuser=True,
        is_staff=True,
    )
    admin.save()


def delete_user(apps, schema_editor=None):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    User.objects.get(email="test_admin@admin.com").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_remove_payment_payments_payment_user"),
    ]

    operations = [
        migrations.RunPython(add_superuser, delete_user),
    ]
