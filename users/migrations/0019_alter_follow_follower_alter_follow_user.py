# Generated by Django 4.1 on 2022-08-25 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0018_alter_follow_follower_alter_follow_user"),
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
