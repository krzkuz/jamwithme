# Generated by Django 4.1 on 2022-08-25 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0016_remove_profile_followers_remove_profile_following_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follow",
            name="follower",
            field=models.ManyToManyField(related_name="follower", to="users.profile"),
        ),
        migrations.AlterField(
            model_name="follow",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
    ]
