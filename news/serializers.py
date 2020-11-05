from rest_framework import serializers
from .models import News,Category

class NewsSerializers(serializers.ModelSerializer):

    class Meta:
        fields=('id','title','category',
                    'created_at','update_at','is_published',
                    'views','photo',)
        model=News

