from django.db import models


# Create your models here.
class NodeType(models.Model):
    """
    NodeType
    -----------
    Describes the type of this machine.

    Parameters
    -----------
    """
    is_client = models.BooleanField(default=False)
    is_balancer = models.BooleanField(default=False)
    is_scaler = models.BooleanField(default=False)


