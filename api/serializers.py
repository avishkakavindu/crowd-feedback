from rest_framework import serializers
from .models import *


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    isCrowded = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'location', 'max_crowd', 'current_crowd', 'isCrowded']

    def get_isCrowded(self, obj):
        return obj.current_crowd >= obj.max_crowd