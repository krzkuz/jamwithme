# Generated by Django 4.1.2 on 2022-11-19 16:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('not_show_for', models.ManyToManyField(blank=True, related_name='not_show_conversation', to='users.profile')),
                ('participants', models.ManyToManyField(blank=True, to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('body', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('conversation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.conversation')),
                ('not_show_for', models.ManyToManyField(blank=True, related_name='not_show_message', to='users.profile')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
