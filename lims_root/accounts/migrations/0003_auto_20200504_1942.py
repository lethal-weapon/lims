# Generated by Django 3.0.4 on 2020-05-04 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200423_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='limit',
            field=models.IntegerField(default=0, verbose_name='Facility Borrow Limit'),
        ),
    ]