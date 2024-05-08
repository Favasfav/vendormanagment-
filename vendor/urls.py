from django.urls import path, include
from .views import (
    VenderAPIview,
    LoginView,
    LogoutView,
    VenderlistAPIview,
    PurchaseOrderView,
    PurchaseOrderViewlist,
    VendorPerformenceView,
)
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("vendor/", VenderAPIview.as_view()),
    path("vendor/<int:pk>/", VenderlistAPIview.as_view()),
    # path('vendor/', VenderAPIview.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("purchaseorder/", PurchaseOrderView.as_view()),
    path("purchaseorder/<int:pk>/", PurchaseOrderView.as_view()),
    path("purchaseorderlist/<int:pk>/", PurchaseOrderViewlist.as_view()),
    path("vendors/<int:pk>/performance", VendorPerformenceView.as_view()),
]
