from django.urls import path
from .views import PurchaseListAPIView, AnalyticListAPIView, ChecksCreateAPIView

urlpatterns = [
    path('places/', PurchaseListAPIView.as_view(), name="places"),
    path('analytics/', AnalyticListAPIView.as_view(), name="analytics"),
    path('add_checks/', ChecksCreateAPIView.as_view(), name="checks"),
]
