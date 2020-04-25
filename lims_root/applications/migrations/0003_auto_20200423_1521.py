# Generated by Django 3.0.4 on 2020-04-23 15:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20200423_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='submitted',
        ),
        migrations.AddField(
            model_name='application',
            name='applied_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Apply Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facilityapplication',
            name='alias',
            field=models.CharField(default='My Application', max_length=50),
        ),
        migrations.AlterField(
            model_name='application',
            name='reply',
            field=models.TextField(blank=True, null=True, verbose_name='Staff Reply'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('PEN', 'PENDING'), ('APP', 'APPLIED'), ('WAI', 'WAITING'), ('ONG', 'ONGOING'), ('BOR', 'BORROWED'), ('OVE', 'OVERTIME'), ('CLO', 'CLOSED')], default='PEN', max_length=3),
        ),
    ]