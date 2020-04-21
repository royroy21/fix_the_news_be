# Generated by Django 3.0.4 on 2020-04-21 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news_items', '0002_added_related_name_to_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('hostname', models.CharField(max_length=254)),
                ('formatted_name', models.CharField(blank=True, default='', max_length=254)),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='favicons')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newsitem',
            name='news_source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='news_items', to='news_items.NewsSource'),
            preserve_default=False,
        ),
    ]
