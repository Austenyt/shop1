from django.urls import path

from goods.apps import GoodsConfig
from goods.views import IndexView, CategoryListView, ProductCreateView, \
    ProductUpdateView, \
    ProductDeleteView, BlogListView, ContactsView, BlogCreateView, BlogUpdateView, BlogDetailView, \
    BlogDeleteView, ProductDetailView, CategoryDetailView

app_name = GoodsConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('goods/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('goods/create', ProductCreateView.as_view(), name='product_create'),
    path('goods/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('goods/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('blog_list', BlogListView.as_view(), name='blog_list'),
    path('blog_view/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
    path('goods/blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('goods/blog_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('goods/blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
