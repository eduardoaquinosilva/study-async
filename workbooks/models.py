from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Workbook(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='workbooks')

    def __str__(self):
        return self.title

class WorkbookView(models.Model):
    ip = models.GenericIPAddressField()
    workbook = models.ForeignKey(Workbook, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ip
