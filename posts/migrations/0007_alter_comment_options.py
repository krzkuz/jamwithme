# Generated by Django 4.1.2 on 2022-10-13 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_comment_dislikes_comment_likes_post_dislikes_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
    ]