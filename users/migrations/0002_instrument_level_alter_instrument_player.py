# Generated by Django 4.1 on 2022-08-14 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="instrument",
            name="level",
            field=models.DecimalField(
                blank=True, decimal_places=0, max_digits=1, null=True
            ),
        ),
        migrations.AlterField(
            model_name="instrument",
            name="player",
            field=models.ManyToManyField(blank=True, to="users.profile"),
        ),
    ]
