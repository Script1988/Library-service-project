# Generated by Django 4.1.5 on 2023-02-16 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=4)),
                ("payment_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-payment_date"],
            },
        ),
        migrations.AddField(
            model_name="user",
            name="payments",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment",
                to="user.payment",
            ),
        ),
    ]
