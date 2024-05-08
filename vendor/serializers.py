from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    SerializerMethodField,
)
from rest_framework import serializers
from .models import Vendor, User, PurchaseOrder, HistoryPerfomence
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class Vendorserializer(ModelSerializer):

    class Meta:
        model = Vendor
        fields = ["name", "contact_details", "address"]


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_username(self, value):
        """
        Check if the username is already in use.
        """
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username is already in use.")
        return value

    def validate_email(self, value):
        """
        Check if the email is already in use.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        # ...

        return token


class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = Vendorserializer()

    class Meta:
        model = PurchaseOrder
        fields = "__all__"

    def create(self, validated_data):
        
        vendor_data = validated_data.pop("vendor")
      
        if Vendor.objects.get(name=vendor_data.get("name")):
            vendor = Vendor.objects.get(name=vendor_data.get("name"))
        else:
            vendor = Vendor.objects.create(**vendor_data)
        qty = 0
        for i in validated_data.get("items"):
            qty = validated_data.get("items")[i]["qty"]

        purchase_order = PurchaseOrder.objects.create(vendor=vendor, **validated_data)
        purchase_order.quantity = qty
        purchase_order.save()
        return purchase_order


class HistorySerializer(serializers.ModelSerializer):
    vendor = Vendorserializer()
    average_response_time = SerializerMethodField()

    class Meta:
        model = HistoryPerfomence
        fields = [
            "vendor",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]

    def get_average_response_time(self, instance):
        time = instance.average_response_time
        day = time // (24 * 3600)

        time = time % (24 * 3600)

        hour = time // 3600

        time %= 3600

        minutes = time // 60

        time %= 60

        seconds = time


        return "d:h:m:s-> %d:%d:%d:%d" % (day, hour, minutes, seconds)
