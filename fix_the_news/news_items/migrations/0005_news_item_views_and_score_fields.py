# Generated by Django 3.0.4 on 2020-08-10 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_items', '0004_remove_news_type_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='newsitem',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
