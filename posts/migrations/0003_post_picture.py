# Generated by Django 4.1 on 2022-08-22 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_alter_post_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to="posts/"),
        ),
    ]
