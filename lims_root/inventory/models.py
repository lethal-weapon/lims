from django.db import models

from accounts.models import Account, SCHOOL_CHOICES


class Apparatus(models.Model):
    name = models.CharField(max_length=100)
    model_no = models.CharField(max_length=50)
    purchased = models.DateField()
    cost = models.DecimalField(decimal_places=2, max_digits=10,
                               blank=True, default=0)

    school = models.CharField(max_length=4, choices=SCHOOL_CHOICES, default='TBD')
    staff = models.ForeignKey(Account, blank=True,
                              null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id)


class Laboratory(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    capacity = models.IntegerField(default=5)

    school = models.CharField(max_length=4, choices=SCHOOL_CHOICES, default='TBD')
    staff = models.ForeignKey(Account, blank=True,
                              null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id)
