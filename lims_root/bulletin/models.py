from django.db import models

from accounts.models import SCHOOL_CHOICES


class Article(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class FacilitySchedule(models.Model):
    school = models.CharField(max_length=4, choices=SCHOOL_CHOICES, default='TBD')
    site = models.CharField(max_length=100, verbose_name='Location', default='DS')
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return str(self.id)
