# Generated by Django 5.1.2 on 2024-10-21 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0003_remove_container_attachments"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ContainerAttachment",
        ),
    ]
