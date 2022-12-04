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
    node_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_client = models.BooleanField(default=False)
    is_balancer = models.BooleanField(default=False)
    is_scaler = models.BooleanField(default=False)


class Credentials(models.Model):
    """
    NodeType
    -----------
    Describes the type of this machine.

    Parameters
    -----------
    """
    token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    token_uri = models.CharField(max_length=100)
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    scopes = models.CharField(max_length=100)

    def save_credentials(self, credentials):
        self.token: credentials.token
        self.refresh_token: credentials.refresh_token
        self.token_uri: credentials.token_uri
        self.client_id: credentials.client_id
        self.client_secret: credentials.client_secret
        self.scopes: credentials.scopes

        self.save()
        return self

    def to_dict(self):
        return {'token': self.token, 'refresh_token': self.refresh_token, 'token_uri': self.token_uri,
                'client_id': self.client_id, 'client_secret': self.client_secret, 'scopes': self.scopes}
