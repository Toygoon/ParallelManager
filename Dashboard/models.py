from django.db import models

 
# Create your models here.
class UsageCPU(models.Model):
    usage = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)


class ClientInfo(models.Model):
    internal_ip = models.CharField(max_length=50)
    external_ip = models.CharField(max_length=50)
