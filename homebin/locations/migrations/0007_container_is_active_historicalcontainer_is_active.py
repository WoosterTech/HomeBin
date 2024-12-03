# Generated by Django 5.1.2 on 2024-12-02 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0006_historicallocation_is_active_location_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Active"),
        ),
        migrations.AddField(
            model_name="historicalcontainer",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Active"),
        ),
    ]