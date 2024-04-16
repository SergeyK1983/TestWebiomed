from rest_framework import generics, status, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Transaction, Product
from .serializer import TransactionSerializer


class TransList(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    # renderer_classes = [JSONRenderer]
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)  # , headers=headers


