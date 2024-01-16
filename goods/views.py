from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView

from goods.models import Category, Product


def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Магазин для фанатов кантри'
    }
    return render(request, 'goods/index.html', context)


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


# def categories(request):
#     context = {
#         'object_list': Category.objects.all(),
#         'title': 'Категории'
#     }
#     return render(request, 'goods/categories.html', context)


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Категории'
    }


# def category_goods(request, pk):
#     category_item = Category.objects.get(pk=pk)
#     context = {
#         'object_list': Product.objects.filter(category_id=pk),
#         'title': f'Категория с товарами - {category_item.name}'
#     }
#     return render(request, 'goods/products.html', context)


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = f'Категория с товарами - {category_item.name}'

        return context_data


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'category',)
    successful_url = reverse_lazy('goods:categories')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'category',)

    def get_success_url(self):
        return reverse('goods:category', args=[self.object.category.pk])


class ProductDeleteView(UpdateView):
    model = Product
    successful_url = reverse_lazy('goods:categories')

# def product(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     return render(request, 'goods/product.html', {'product': product_item})
