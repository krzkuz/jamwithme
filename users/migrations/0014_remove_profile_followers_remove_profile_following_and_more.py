# Generated by Django 4.1 on 2022-08-25 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_remove_profile_friend_profile_followers_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="profile", name="followers",),
        migrations.RemoveField(model_name="profile", name="following",),
        migrations.AddField(
            model_name="profile",
            name="followers",
            field=models.ManyToManyField(
                blank=True, related_name="followers", to="users.profile"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="following",
            field=models.ManyToManyField(
                blank=True, related_name="following", to="users.profile"
            ),
        ),
    ]
