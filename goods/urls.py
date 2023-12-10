from django.urls import path

from goods.apps import GoodsConfig
from goods.views import index, categories, category_goods, products_goods, contact

app_name = GoodsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('categories/', categories, name='categories'),
    path('<int:pk>/goods/', category_goods, name='category_goods'),
    path('<int:pk>/products/', products_goods, name='products'),
]
