# Generated by Django 4.1 on 2022-08-17 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_profile_friend"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="friend",
            field=models.ManyToManyField(blank=True, to="users.profile"),
        ),
    ]
