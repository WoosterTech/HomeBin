# Generated by Django 5.1.2 on 2024-10-21 17:09
# move attachments from ManyToManyField to GenericRelation
# old model attachments.Attachment; new model attachments.GenericAttachment

from django.apps.registry import Apps
from django.contrib.contenttypes.models import ContentType

from django.db import migrations


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def move_attachments(apps: Apps, _):
    Container = apps.get_model("locations", "Container")
    GenericAttachment = apps.get_model(
        "attachments",
        "GenericAttachment"
    )
    container_type = ContentType.objects.get(app_label="locations", model="container")
    logger.info("ContentType for Container: %s", type(container_type))

    for container in Container.objects.all():
        logger.info("Moving attachments for container %s", container.label)
        for attachment in container.attachments.all():
            logger.info("Moving attachment %s", attachment.name)
            _, _ = GenericAttachment.objects.update_or_create(
                content_type_id = container_type.pk,
                object_id = container.pk,
                file=attachment.attachment,
                defaults={
                    "name": attachment.name,
                    "attachment_type": attachment.type,
                },
            )
            attachment.delete()

class Migration(migrations.Migration):

    dependencies = [
        ("attachments", "0006_alter_attachment_type_and_more"),
    ]

    operations = []
