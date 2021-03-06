# Generated by Django 3.0.4 on 2020-05-30 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_added_verbose_name_plural_categories'),
        ('comments', '0003_comments_use_foreign_keys'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='topics.Topic'),
        ),
    ]
