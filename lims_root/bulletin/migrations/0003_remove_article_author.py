# Generated by Django 3.0.4 on 2020-04-13 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0002_auto_20200413_0624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
    ]