# Generated by Django 5.1.2 on 2024-11-04 21:30

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0002_manufacturer_asset_model_historicalasset_model_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="manufacturer",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True, editable=False, populate_from="name"
            ),
        ),
        migrations.AlterField(
            model_name="manufacturer",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
