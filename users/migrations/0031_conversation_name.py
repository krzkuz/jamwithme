# Generated by Django 4.1 on 2022-08-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0030_remove_conversation_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="name",
            field=models.CharField(
                blank=True, default="noname", max_length=250, null=True
            ),
        ),
    ]
