from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView, DetailView

from goods.forms import VersionForm, ProductForm
from goods.models import Category, Product, Blog, Version


class IndexView(TemplateView):
    template_name = 'goods/index.html'
    extra_context = {
        'title': 'Магазин для фанатов кантри'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]
        return context_data


# def index(request):
#     context = {
#         'object_list': Category.objects.all()[:3],
#         'title': 'Магазин для фанатов кантри'
#     }
#     return render(request, 'goods/index.html', context)

class ContactsView(View):
    template_name = 'goods/contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Контакты'})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

        return render(request, self.template_name, {'title': 'Контакты'})


# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         print(f'{name} ({email}): {message}')
#
#     context = {
#         'title': 'Контакты'
#     }
#     return render(request, 'goods/contacts.html', context)


# def categories(request):
#     context = {
#         'object_list': Category.objects.all(),
#         'title': 'Категории'
#     }
#     return render(request, 'goods/category_list.html', context)


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
#     return render(request, 'goods/category_detail.html', context)


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        product_items = Product.objects.filter(category=self.object)
        context_data['product_items'] = product_items
        context_data['title'] = f'Категория с товарами - {self.object.name}'

        return context_data


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def product_detail_view(request, product_id):
        product = Product.objects.get(pk=product_id)
        versions = product.get_versions()  # Получаем все версии продукта
        context = {
            'product': product,
            'versions': versions,  # Передаем версии продукта в контекст
        }
        return render(request, 'category_detail.html', context)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(category_id=self.kwargs.get('pk'))
    #     return queryset

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(*args, **kwargs)
    #
    #     category_item = Category.objects.get(pk=self.kwargs.get('pk'))
    #     context_data['category_pk'] = category_item.pk,
    #     context_data['title'] = f'Категория с товарами - {category_item.name}'

    # return context_data


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('goods:index')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def get_success_url(self):
        return reverse('goods:product_update', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save(commit=False)
        self.object.author = self.request.user  # Привязка продукта к авторизованному пользователю
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    successful_url = reverse_lazy('goods:contacts')


# def product(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     return render(request, 'goods/product_detail.html', {'product': product_item})


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'body', 'preview',)
    success_url = reverse_lazy('goods:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'preview',)

    # success_url = reverse_lazy('goods:blog_view')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('goods:blog_view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('goods:blog_list')
