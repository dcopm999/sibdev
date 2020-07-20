from customers import models
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class GemsSerializer(serializers.Serializer):
    response = serializers.ListField()


class CustomerSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = models.Customer
        fields = "__all__"


class DealsUploadSerializer(serializers.Serializer):
    deals = serializers.FileField()

    class Meta:
        fields = ("deals",)
