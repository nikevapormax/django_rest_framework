from django.forms import modelformset_factory
from rest_framework import serializers

from .models import Product as ProductModel
from user.models import User as UserModel

class ProductSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    # def get_user(self, obj):
    #     print(obj)
    #     user = self.context["request"].user
    #     return user.username
    
    class Meta:
        model = ProductModel
        fields = ["user", "title", "thumbnail", "desc", "exposure_start", "exposure_end"]
        
