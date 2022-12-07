import json

from API.models import ClientNodes
from Initializer.models import NodeType
from Initializer.utils import request_cred


def refresh_info():
    node = NodeType.objects.all().last()
    response = request_cred(f'https://compute.googleapis.com/compute/v1/projects/{node.server_ip}/zones/asia-northeast3-a/instances')

    if response.status_code == 401:
        return False

    x = json.loads(response.text)

    ClientNodes.objects.all().delete()

    for item in x['items']:
        c = ClientNodes()
        c.node_name = item['name']
        c.client_id = item['id']
        c.internal_ip = item['networkInterfaces'][0]['networkIP']
        c.external_ip = item['networkInterfaces'][0]['accessConfigs'][0]['natIP']

        tmp = item['creationTimestamp']
        c.created_at = tmp[:tmp.find('T')]

        tmp = item['machineType']
        c.machine_type = tmp[tmp.rfind('/')+1:]

        c.status = item['status']
        c.save()

