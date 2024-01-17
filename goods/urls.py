from django.urls import path

from goods.apps import GoodsConfig
from goods.views import IndexView, CategoryListView, ProductListView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, BlogListView, ContactsView

app_name = GoodsConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('goods/<int:pk>/', ProductListView.as_view(), name='category_goods'),
    path('goods/create', ProductCreateView.as_view(), name='product_create'),
    path('goods/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('goods/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
]
