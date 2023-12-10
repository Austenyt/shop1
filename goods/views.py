from django.shortcuts import render

from goods.models import Category, Product


def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Магазин для фанатов кантри'
    }
    return render(request, 'goods/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'goods/contact.html', context)


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
        'title': f'Категория - {category_item.name}'
    }
    return render(request, 'goods/categories.html', context)


def products_goods(request, pk):
    context = {
        'object': Product.objects.get(pk=pk),
        'title': f'Продукт'
    }
    return render(request, 'goods/product.html', context)
