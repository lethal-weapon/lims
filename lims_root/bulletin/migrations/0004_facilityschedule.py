# Generated by Django 3.0.4 on 2020-04-17 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0003_remove_article_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilitySchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(choices=[('CS', 'Computer Science'), ('CE', 'Communication Engineering'), ('OE', 'OptoElectronic Engineering'), ('SE', 'Big Data and Software Engineering'), ('AUTO', 'Automation'), ('TBD', 'Unknown')], default='TBD', max_length=4)),
                ('site', models.CharField(default='Meeting point', max_length=100, verbose_name='Location')),
                ('day', models.DateField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
            ],
        ),
    ]
