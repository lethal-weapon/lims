from django.db import models

from accounts.models import Account
from inventory.models import Facility

STATUS_CHOICES = (
    ('APP', 'APPLIED'),
    ('WAI', 'WAITING'),
    ('ONG', 'ONGOING'),
    ('BOR', 'BORROWED'),
    ('OVE', 'OVERTIME'),
    ('CLO', 'CLOSED'),
)


class Application(models.Model):
    start = models.DateField(verbose_name='Start Date')
    end = models.DateField(verbose_name='End Date')
    submitted = models.DateTimeField(verbose_name='Apply Time', auto_now_add=True)

    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='APP')
    reason = models.TextField(verbose_name='Apply Reason')
    reply = models.CharField(verbose_name='Staff Short Reply', max_length=100, blank=True, null=True)

    applicant = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class FacilityApplication(Application):
    items = models.ManyToManyField(Facility, verbose_name='Applied Facilities')


class ResearchApplication(Application):
    title = models.CharField(max_length=150, verbose_name='Research Title')
    members = models.ManyToManyField(Account, verbose_name='Team Members')

    def __str__(self):
        return self.title
