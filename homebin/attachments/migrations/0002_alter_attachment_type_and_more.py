# Generated by Django 5.1.2 on 2024-10-17 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attachments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attachment",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("document", "Document"),
                    ("image", "Image"),
                    ("video", "Video"),
                    ("audio", "Audio"),
                ],
                default="image",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="historicalattachment",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("document", "Document"),
                    ("image", "Image"),
                    ("video", "Video"),
                    ("audio", "Audio"),
                ],
                default="image",
                max_length=10,
            ),
        ),
    ]