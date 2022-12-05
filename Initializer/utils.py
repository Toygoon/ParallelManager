import requests

from Initializer.models import NodeType


def not_registered():
    return NodeType.objects.all().last() is None


def not_completed():
    return not NodeType.objects.all().last().reg_completed


def check_ip():
    node = NodeType.objects.all().last()
    r = requests.get(f'{node.server_ip}/api/hello')

    return r.status_code
