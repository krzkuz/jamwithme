# Generated by Django 4.1 on 2022-09-04 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0034_conversation_updated_alter_conversation_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="message", name="conversation",),
        migrations.RemoveField(model_name="message", name="sender",),
        migrations.DeleteModel(name="Conversation",),
        migrations.DeleteModel(name="Message",),
    ]
