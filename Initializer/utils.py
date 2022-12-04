from Initializer.models import NodeType


def not_registered():
    return NodeType.objects.all().last() is None


def not_completed():
    return not NodeType.objects.all().last().reg_completed
