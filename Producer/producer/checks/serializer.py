from rest_framework import serializers
from .models import Transaction, Product


class ProductSerializer(serializers.ModelSerializer):
    """ Продукты в чеке """

    class Meta:
        model = Product
        fields = [
            "product_id",
            "quantity",
            "price",
            "category"
        ]


class TransactionSerializer(serializers.ModelSerializer):
    """ Транзакции """

    items = ProductSerializer(many=True)

    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "timestamp",
            "items",
            "total_amount",
            "nds_amount",
            "tips_amount",
            "payment_method"
        ]

    def create(self, validated_data):
        # print("context: ", self.context['request'].data)
        items = validated_data.pop("items", [])
        instance = Transaction.objects.create(**validated_data)

        list(map(lambda x: x.update({"transaction": instance}), items))
        list_products = [Product(**items[i]) for i in range(len(items))]
        Product.objects.bulk_create(list_products)

        return instance

