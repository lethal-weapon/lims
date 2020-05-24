# Generated by Django 3.0.4 on 2020-05-24 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilitySchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(choices=[('CS', 'Computer Science'), ('CE', 'Communication Engineering'), ('OE', 'OptoElectronic Engineering'), ('SE', 'Big Data and Software Engineering'), ('AUTO', 'Automation'), ('TBD', 'Unknown')], default='TBD', max_length=4)),
                ('site', models.CharField(default='DS', max_length=100, verbose_name='Location')),
                ('day', models.DateField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
