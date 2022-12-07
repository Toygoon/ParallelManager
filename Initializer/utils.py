import json

import requests

from Initializer.models import NodeType, Credentials


def not_registered():
    return NodeType.objects.all().last() is None


def not_completed():
    return not NodeType.objects.all().last().reg_completed


def check_ip(is_project=None):
    node = NodeType.objects.all().last()
    try:
        r = None

        if is_project:
            r = request_cred(f'https://compute.googleapis.com/compute/v1/projects/{node.server_ip}/')
        else:
            r = requests.get(f'http://{node.server_ip}:8000/api/hello')
    except:
        return False

    return r.status_code


def request_cred(url: str):
    c = Credentials.objects.all().last()
    r = requests.get(url, headers={'Authorization': 'Bearer ' + c.token})

    return r
