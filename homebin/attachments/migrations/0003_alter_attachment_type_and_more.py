# Generated by Django 5.1.2 on 2024-10-17 23:22

import django.db.models.deletion
import homebin.attachments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attachments", "0002_alter_attachment_type_and_more"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attachment",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("video", "Video"),
                    ("document", "Document"),
                    ("audio", "Audio"),
                    ("image", "Image"),
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
                    ("video", "Video"),
                    ("document", "Document"),
                    ("audio", "Audio"),
                    ("image", "Image"),
                ],
                default="image",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="GenericAttachment",
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
                (
                    "file",
                    models.FileField(
                        upload_to=homebin.attachments.models.attachment_upload_to
                    ),
                ),
                ("name", models.CharField(editable=False, max_length=100)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("object_id", models.PositiveIntegerField()),
                (
                    "attachment_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("video", "Video"),
                            ("document", "Document"),
                            ("audio", "Audio"),
                            ("image", "Image"),
                        ],
                        default="image",
                        max_length=10,
                    ),
                ),
                ("sort_rank", models.PositiveIntegerField(db_index=True, default=0)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_rank"],
                "indexes": [
                    models.Index(
                        fields=["content_type", "object_id"],
                        name="attachments_content_c34382_idx",
                    )
                ],
            },
        ),
    ]
