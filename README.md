## "Тестовое задание"

## Реализация сервисов с использованием Apache Kafka, Django, Celery

---

### Первый сервис (Producer). Прием чеков покупок клиентов
### Второй сервис (Consumer). Прием чеков из первого сервиса посредством Apache Kafka. Аналитика.

___

Развертывание
1. Из корневой директории "docker-compose up" (контейнер с Apache Kafka)
2. Из директории Producer "docker-compose up" (контейнер с 1 сервисом)
3. Из директории Consumer "docker-compose up" (контейнер с 2 сервисом)

Документация 1 сервис: http://localhost:8000/swagger/ \
Документация 2 сервис: http://localhost:9000/swagger/ \
Файлы .env выложил, чтобы не было дополнительных доработок.

---

Эндпоинты:

1 Сервис:\
POST http://localhost:8000/api/checks/ - отправка чеков

2 Сервис:\
GET http://localhost:9000/api/places/ - просмотр мест покупок\
GET http://localhost:9000/api/analytics/ - просмотр общей аналитики\
GET http://localhost:9000/api/analytics/<str:place_id>/ - просмотр общей аналитики по месту покупки\
POST http://localhost:9000/api/add_checks/ - принять чек
POST http://localhost:9000/auth/login/
POST http://localhost:9000/auth/registration/

---
Пример чека (для обоих сервисов)

    {
        "transaction_id": "unique_transaction_id2",
        "timestamp": "2024-02-07T12:34:56",
        "items": [
            {
                "product_id": "product_id_1",
                "quantity": 2,
                "price": 10.49,
                "category": "tanks"
            },
            {
                "product_id": "product_id_1",
                "quantity": 1,
                "price": 5.49,
                "category": "plane"
            }
        ],
        "total_amount": 250,
        "nds_amount": 2.47,
        "tips_amount": 3.0,
        "payment_method": "credit_card",
        "place_id": "011",
        "place_name": "Магазин №1"
    }

Указанные поля обязательны, по ним выполняется валидация. Дополнительные поля значения не имеют.

