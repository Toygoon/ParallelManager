import requests

from Initializer.models import NodeType


def not_registered():
    return NodeType.objects.all().last() is None


def not_completed():
    return not NodeType.objects.all().last().reg_completed


def check_ip():
    node = NodeType.objects.all().last()
    try:
        r = requests.get(f'http://{node.server_ip}:8000/api/hello')
    except:
        return False

    return r.status_code
