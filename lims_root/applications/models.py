# from django.db import models
#
# from accounts.models import Account
# from inventory.models import Apparatus, Laboratory
#
#
# class Application(models.Model):
#     start = models.DateField(verbose_name='Start Date')
#     end = models.DateField(verbose_name='End Date')
#     submitted = models.DateTimeField(verbose_name='Apply Time', auto_now_add=True)
#
#     reason = models.TextField(verbose_name='Apply Reason')
#     reply = models.CharField(verbose_name='Staff Short Reply', max_length=100,
#                              blank=True, null=True)
#
#     staff = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
#     applicant = models.ForeignKey(Account, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.id)
