# Generated by Django 4.1 on 2022-08-27 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0025_remove_conversation_participants_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="name",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
