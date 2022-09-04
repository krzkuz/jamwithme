# Generated by Django 4.1 on 2022-09-04 10:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0035_remove_message_conversation_remove_message_sender_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Conversation",
            fields=[
                ("name", models.CharField(blank=True, max_length=250, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(blank=True, to="users.profile"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("body", models.TextField(null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "conversation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="chat.conversation",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.profile",
                    ),
                ),
            ],
            options={"ordering": ["created"],},
        ),
    ]
