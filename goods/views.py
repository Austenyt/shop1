from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from goods.models import Category, Product


class CategoriesListView(ListView):
    model = Product
    template_name = 'goods/index.html'


# def index(request):
#     context = {
#         'object_list': Category.objects.all()[:3],
#         'title': 'Магазин для фанатов кантри'
#     }
#     return render(request, 'goods/index.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'goods/contacts.html', context)


def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Категории'
    }
    return render(request, 'goods/categories.html', context)


def category_goods(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': f'Категория с товарами - {category_item.name}'
    }
    return render(request, 'goods/products.html', context)


def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    return render(request, 'goods/product.html', {'product': product_item})
