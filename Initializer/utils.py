from Initializer.models import NodeType


def not_registered():
    node = NodeType.objects.all().last()
    return node is None or not node.reg_completed
