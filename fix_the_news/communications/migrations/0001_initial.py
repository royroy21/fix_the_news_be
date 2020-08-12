# Generated by Django 3.0.4 on 2020-08-12 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False, help_text='Setting a communication to active will set all other communications of the same type to False. The frontend app will be update next time it calls the user API')),
                ('text', models.TextField()),
                ('type', models.CharField(choices=[('welcome', 'welcome'), ('daily', 'daily')], max_length=7)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
