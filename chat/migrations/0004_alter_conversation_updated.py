# Generated by Django 4.1.2 on 2022-10-13 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_conversation_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='updated',
            field=models.DateTimeField(null=True),
        ),
    ]
