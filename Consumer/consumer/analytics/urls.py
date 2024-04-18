from django.urls import path
from .views import PurchaseListAPIView, AnalyticListAPIView, AnalyticPurchaseLocationListAPIView, ChecksCreateAPIView

urlpatterns = [
    path('places/', PurchaseListAPIView.as_view(), name="places"),
    path('analytics/', AnalyticListAPIView.as_view(), name="analytics"),
    path('analytics/<str:place_id>/', AnalyticPurchaseLocationListAPIView.as_view(), name="analytics-place-id"),
    path('add_checks/', ChecksCreateAPIView.as_view(), name="checks"),
]
