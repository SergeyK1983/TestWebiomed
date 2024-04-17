from datetime import datetime
from .models import PurchaseLocation, Category, Taxes, CategoryAnalytic


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


def purchase_location_methods(value):
    """ Методы модели PurchaseLocation """

    value.total_purchases = value.get_total_purchases()
    value.average_receipt = value.get_average_receipt()
    value.save()
    return None


def taxes_methods(value, time_now):
    """ Методы модели Taxes """

    taxes = Taxes(location=value)
    taxes.total_nds = taxes.get_total_nds(time_now)
    taxes.total_tips = taxes.get_total_tips(time_now)
    taxes.save()
    return None


def category_analytic_methods(value, time_now):
    """ Методы модели CategoryAnalytic """

    cat_analytic = CategoryAnalytic(cat=value)
    analytic = cat_analytic.get_total_spent_and_average_receipt(time_now)
    cat_analytic.total_spent = analytic["total_spent"]
    cat_analytic.average_receipt = analytic["average_receipt"]
    cat_analytic.save()
    return None


def get_analytic_methods():
    """ Расчет значений аналитических методов и запись в БД """

    time_now = datetime.now()
    purchase = PurchaseLocation.objects.all()
    categories = Category.objects.all()

    for value in purchase:
        purchase_location_methods(value)
        taxes_methods(value, time_now)

    for value in categories:
        category_analytic_methods(value, time_now)

    return None
