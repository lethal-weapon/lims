# Generated by Django 3.0.4 on 2020-04-09 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True)),
                ('campus_id', models.CharField(max_length=30, unique=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('school', models.CharField(choices=[('CS', 'Computer Science'), ('CE', 'Communication Engineering'), ('OE', 'OptoElectronic Engineering'), ('SE', 'Big Data and Software Engineering'), ('AUTO', 'Automation')], max_length=4)),
                ('borrow_limit', models.IntegerField(default=2)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]