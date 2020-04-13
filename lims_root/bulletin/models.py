from django.db import models


class Article(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
