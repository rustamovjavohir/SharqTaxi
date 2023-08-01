from apps.file.models import Image
from rest_framework.serializers import ModelSerializer


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('id',
                  'name',
                  'image',
                  'is_main',
                  'created_at')
