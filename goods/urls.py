from django.urls import path

from goods.apps import GoodsConfig
from goods.views import IndexView, CategoryListView, ProductListView, ProductDetailView, ProductCreateView, \
    ProductUpdateView, \
    ProductDeleteView, BlogListView, ContactsView, CategoryDetailView, BlogCreateView

app_name = GoodsConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('goods/', ProductListView.as_view(), name='products'),
    path('goods/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('goods/create', ProductCreateView.as_view(), name='product_create'),
    path('goods/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('goods/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/', BlogCreateView.as_view(), name='blog_list'),

]
