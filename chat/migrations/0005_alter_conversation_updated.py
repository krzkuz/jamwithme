# Generated by Django 4.1.2 on 2022-10-13 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_conversation_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
