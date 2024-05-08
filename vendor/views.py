from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import (
    Vendorserializer,
    UserSerializer,
    LoginSerializer,
    MyTokenObtainPairSerializer,
    PurchaseOrderSerializer,
    HistorySerializer,
)
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile, Vendor, PurchaseOrder, HistoryPerfomence
import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.forms import model_to_dict

# Create your views here.


from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LoginView(APIView):
    def post(self, request):

        try:
            print(request.data)
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                username = request.data.get("username")
                password = request.data.get("password")
                user = authenticate(username=username, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                print(token)
                response = Response()
                response.set_cookie(key="jwt", value=token)
                return response

            # else:
            #     return JsonResponse({'success': 'false', 'msg': 'The credentials provided are invalid.'})

        except Exception as e:
            return Response({"e": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            jwt_cookie = request.COOKIES.get("jwt")
            print(jwt_cookie)

            response = Response()
            response.delete_cookie("jwt")

            return Response(response.cookies, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class VenderAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        request.data._mutable = True
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            name = request.data.get("username")
            request.data["name"] = name
            request.data._mutable = False
            serializer1 = Vendorserializer(data=request.data)
            if serializer1.is_valid():

                vendor = Vendor.objects.create(
                    name=request.data["name"],
                    contact_details=request.data["contact_details"],
                    address=request.data["address"],
                )  # Create vendor instance
                UserProfile.objects.create(user=user, vendor=vendor)
            return Response(
                {"message": serializer.data}, status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        permission_classes = [IsAuthenticated]
        try:

            queiryset = Vendor.objects.all()
            print(queiryset)
            serializer = Vendorserializer(queiryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        permission_classes = [IsAuthenticated]
        try:

            queryset = Vendor.objects.get(id=pk)

            serializer = Vendorserializer(instance=queryset, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None) -> Response:
        permission_classes = [IsAuthenticated]
        obj = Vendor.objects.get(id=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VenderlistAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None) -> Response:

        try:

            queryset = Vendor.objects.get(id=pk)
            serializer = Vendorserializer(instance=queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None) -> Response:
        permission_classes = [IsAuthenticated]
        try:
            obj = Vendor.objects.get(id=pk)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            obj = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(instance=obj, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        print(request.data)
        try:

            serializer = PurchaseOrderSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                print(serializer.validated_data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        try:

            obj = PurchaseOrder.objects.get(id=pk)
            print(obj, pk)
            serializer = PurchaseOrderSerializer(
                instance=obj, data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        permission_classes = [IsAuthenticated]
        try:
            obj = PurchaseOrder.objects.get(id=pk)
            obj.delete()
            return Response(
                {"message": "susussfully deleted"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderViewlist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            obj = PurchaseOrder.objects.get(id=pk)
            serializer = PurchaseOrderSerializer(instance=obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VendorPerformenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            print("kkkk")
            obj = HistoryPerfomence.objects.get(vendor=pk)
            print("kkkk", obj)

            serializer = HistorySerializer(instance=obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
