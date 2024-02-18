from django.urls import path
from django.views.decorators.cache import cache_page

from goods.apps import GoodsConfig
from goods.views import IndexView, CategoryListView, ProductDetailView, ProductCreateView, \
    ProductUpdateView, \
    ProductDeleteView, BlogListView, ContactsView, BlogCreateView, BlogUpdateView, BlogDetailView, \
    BlogDeleteView, ProductListView

app_name = GoodsConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', ProductListView.as_view(), name='product_list'),
    path('goods/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('goods/create', ProductCreateView.as_view(), name='product_create'),
    path('goods/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('goods/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('blog_list', BlogListView.as_view(), name='blog_list'),
    path('blog_view/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
    path('goods/blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('goods/blog_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('goods/blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
