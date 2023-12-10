from django.core.management import BaseCommand

from goods.models import Category, Product


class Command(BaseCommand):

    Category.objects.all().delete()
    Product.objects.all().delete()

    def handle(self, *args, **options):
        category_list = [
            {'pk': 1, 'name': 'Музыкальные инструменты'},
            {'pk': 2, 'name': 'Для машины'},
            {'pk': 3, 'name': 'Одежда'}
        ]

        category_for_create = []
        for category_item in category_list:
            category_for_create.append(
                Category(**category_item)
            )

        Category.objects.bulk_create(category_for_create)

        product_list = [


        ]

        product_for_create = []
        for product_item in product_list:
            product_for_create.append(
                Product(**product_item)
            )

        Product.objects.bulk_create(product_for_create)
