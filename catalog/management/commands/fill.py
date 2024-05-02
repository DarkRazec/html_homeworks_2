import json

from django.core.management import BaseCommand

from catalog.models import Category, Contact


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

        Contact.objects.all().delete()
        Category.objects.all().delete()

        # Списки для хранения объектов
        category_for_create = [Category(
            id=category['pk'],
            **category['fields']
        ) for category in Command.json_read_categories()]

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        product_for_create = [Contact(
            id=product['pk'],
            name=product['fields']['country'],
            desc=product['fields']['desc'],
            category=Category.objects.get(pk=product['fields']['category']),
            price=product['fields']['price']
        ) for product in Command.json_read_products()]

        # Создаем объекты в базе с помощью метода bulk_create()
        Contact.objects.bulk_create(product_for_create)
