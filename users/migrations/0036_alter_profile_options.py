# Generated by Django 4.1.2 on 2022-10-13 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_remove_message_conversation_remove_message_sender_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]
