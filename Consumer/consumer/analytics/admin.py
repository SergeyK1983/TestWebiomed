from django.contrib import admin
from .models import Check, Product, PurchaseLocation, Taxes, Category, CategoryAnalytic


class CheckAdmin(admin.ModelAdmin):
    list_display = ("id", "place_id", "place_name", "total_amount", "nds_amount", "tips_amount", "date_create")
    ordering = ("id", "place_id", "place_name")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "quantity", "price", "category", "to_check", "date_create")
    ordering = ("to_check", )


class PurchaseLocationAdmin(admin.ModelAdmin):
    list_display = ("id", "place_id", "place_name", "total_purchases", "average_receipt")
    ordering = ("place_name", )


class TaxesAdmin(admin.ModelAdmin):
    list_display = ("id", "location", "total_nds", "total_tips")
    ordering = ("location", )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "location", "category")
    ordering = ("location", )


class CategoryAnalyticAdmin(admin.ModelAdmin):
    list_display = ("id", "cat", "total_spent", "average_receipt")
    ordering = ("cat", )


admin.site.register(Check, CheckAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PurchaseLocation, PurchaseLocationAdmin)
admin.site.register(Taxes, TaxesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryAnalytic, CategoryAnalyticAdmin)
