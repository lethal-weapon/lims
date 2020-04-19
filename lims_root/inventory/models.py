from django.db import models

from accounts.models import Account, SCHOOL_CHOICES


class Facility(models.Model):
    name = models.CharField(max_length=100)
    staff = models.ForeignKey(Account, on_delete=models.DO_NOTHING, blank=True, null=True)
    school = models.CharField(max_length=4, choices=SCHOOL_CHOICES, default='TBD')

    def __str__(self):
        return str(self.id)


class Apparatus(Facility):
    cost = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    model_no = models.CharField(max_length=50)
    purchased = models.DateField()


class Laboratory(Facility):
    location = models.CharField(max_length=50)
    capacity = models.IntegerField(default=5)
