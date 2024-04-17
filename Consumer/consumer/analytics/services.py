from .models import PurchaseLocation, Category


def create_category(items) -> None:
    """ Создание записи в модели Category """

    categories = [Category(**items[i]) for i in range(len(items))]
    Category.objects.bulk_create(categories)
    return None


def create_purchase_or_add_category(instance) -> None:
    """ Создание записи о новом месте покупки и соответствующих категориях, либо добавление новой категории товара """

    products = instance.items.all()

    if PurchaseLocation.objects.filter(place_id=instance.place_id).exists():
        purchase = PurchaseLocation.objects.get(place_id=instance.place_id)
        categories = purchase.category_analytics.all().values("category")
        category_name = list(map(lambda x: x.get("category"), categories))

        cat_in_products = [
            {"location": purchase, "category": i.category} for i in products if i.category not in category_name
        ]
        if cat_in_products:
            create_category(cat_in_products)
    else:
        purchase = PurchaseLocation.objects.create(place_id=instance.place_id, place_name=instance.place_name)
        cat_in_products = [{"location": purchase, "category": i.category} for i in products]
        create_category(cat_in_products)
    return None
