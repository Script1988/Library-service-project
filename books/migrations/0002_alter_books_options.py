# Generated by Django 4.1.5 on 2023-01-30 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="books",
            options={"verbose_name_plural": "books"},
        ),
    ]
