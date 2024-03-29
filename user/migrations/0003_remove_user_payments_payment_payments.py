# Generated by Django 4.1.5 on 2023-02-16 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_payment_user_payments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="payments",
        ),
        migrations.AddField(
            model_name="payment",
            name="payments",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
