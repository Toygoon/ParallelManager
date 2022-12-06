from django.db import models


class ClientNodes(models.Model):
    node_name = models.CharField(max_length=50)
    ip = models.CharField(max_length=50)
