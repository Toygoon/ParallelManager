from rest_framework.serializers import ModelSerializer

from Dashboard.models import ClientInfo


class ClientInfoSerializer(ModelSerializer):
    class Meta:
        model = ClientInfo
        fields = '__all__'
