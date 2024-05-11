import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        # Получаем данные из фикстур с категориями
        with open('data/category_data.json', encoding='utf-16') as f:
            return json.load(f)

    @staticmethod
    def json_read_products():
        # Получаем данные из фикстур с продуктами
        with open('data/product_data.json', encoding='utf-16') as f:
            return json.load(f)

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()

        # Списки для хранения объектов
        category_for_create = [Category(
            id=category['pk'],
            **category['fields']
        ) for category in Command.json_read_categories()]

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        product_for_create = [Product(
            id=product['pk'],
            name=product['fields']['name'],
            desc=product['fields']['desc'],
            category=Category.objects.get(pk=product['fields']['category']),
            price=product['fields']['price']
        ) for product in Command.json_read_products()]

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
