from django.urls import path

from goods.apps import GoodsConfig
from goods.views import index, categories, category_goods, contacts, product

app_name = GoodsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contact'),
    path('categories/', categories, name='categories'),
    path('categories/<int:pk>/products/', category_goods, name='category_goods'),
    path('product/<int:pk>/', product, name='product'),
]
