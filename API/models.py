from django.db import models


class ClientNodes(models.Model):
    node_name = models.CharField(max_length=50)
    external_ip = models.CharField(max_length=50)
    internal_ip = models.CharField(max_length=50)
    client_id = models.CharField(max_length=50)
    machine_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateField()


class BenchmarkUUIDs(models.Model):
    recv_uuid = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
