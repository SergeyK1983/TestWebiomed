from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import PurchaseLocation
from .serializer import CheckSerializer, PurchaseLocationSerializer, AnalyticSerializer
from .services import create_purchase_or_add_category


class PurchaseListAPIView(generics.ListAPIView):
    """ Список мест покупок """

    permission_classes = [permissions.AllowAny]
    serializer_class = PurchaseLocationSerializer
    queryset = PurchaseLocation.objects.all()


class AnalyticListAPIView(generics.ListAPIView):
    """ Общая аналитика """

    permission_classes = [permissions.AllowAny]
    serializer_class = AnalyticSerializer
    queryset = PurchaseLocation.objects.all()


class AnalyticPurchaseLocationListAPIView(generics.ListAPIView):
    """ Общая аналитика для места покупки """

    permission_classes = [permissions.AllowAny]
    serializer_class = AnalyticSerializer

    def get_queryset(self):
        queryset = PurchaseLocation.objects.filter(place_id=self.kwargs["place_id"])
        return queryset


class ChecksCreateAPIView(generics.CreateAPIView):
    """ Прием чеков покупок. Запись в БД. """

    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    serializer_class = CheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        create_purchase_or_add_category(instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





