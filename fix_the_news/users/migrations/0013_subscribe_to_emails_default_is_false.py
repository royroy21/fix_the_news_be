# Generated by Django 3.0.7 on 2020-09-05 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_no_upload_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subscribe_to_emails',
            field=models.BooleanField(default=False),
        ),
    ]
