from Initializer.models import NodeType


def not_registered():
    return NodeType.objects.all().last() is None
