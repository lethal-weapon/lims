# Generated by Django 3.0.4 on 2020-04-17 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0004_facilityschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityschedule',
            name='site',
            field=models.CharField(default='DS', max_length=100, verbose_name='Location'),
        ),
    ]
