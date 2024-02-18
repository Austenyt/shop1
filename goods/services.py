from django.core.cache import cache

from config import settings
from goods.models import Category


def get_categories(product_pk):
    if settings.CACHE_ENABLED:
        key = f'category_list{product_pk}'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.filter(product_pk=product_pk)
            cache.set(key, category_list)
    else:
        category_list = Category.objects.filter(product_pk=product_pk)

    return category_list
