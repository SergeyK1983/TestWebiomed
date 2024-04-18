from django.contrib import admin
from .models import Product, Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction_id", "timestamp", "total_amount", "nds_amount", "tips_amount", "payment_method",
                    "place_id", "place_name")
    ordering = ("transaction_id", "timestamp")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_id", "quantity", "price", "category", "transaction")
    ordering = ("product_id", "transaction")
    search_fields = ("category", )


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Product, ProductAdmin)
