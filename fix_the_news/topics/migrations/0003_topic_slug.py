# Generated by Django 3.0.4 on 2020-06-26 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_added_verbose_name_plural_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
    ]
