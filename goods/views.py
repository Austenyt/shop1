from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView, DetailView

from goods.forms import VersionForm, ProductForm
from goods.models import Category, Product, Blog, Version


class IndexView(TemplateView):      # Главная страница
    template_name = 'goods/index.html'
    extra_context = {
        'title': 'Магазин для фанатов кантри'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]
        return context_data


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


class CategoryListView(ListView):   # Категории в главном выпадающем меню
    model = Category
    extra_context = {
        'title': 'Категории'
    }


class ProductListView(LoginRequiredMixin, ListView):   # Cписок товаров при нажатии "Открыть" в списке категорий
    model = Product

    # def get_queryset(self):
    #     return super().get_queryset().filter(
    #         category_id=self.kwargs.get('pk'),
    #         owner=self.request.user
    #     )

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk
        context_data['title'] = f'Категория с товарами {category_item.name}'
        return context_data


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'goods/product_detail.html'
    context_object_name = 'product'

    def product_detail_view(request, product_id):
        product = Product.objects.get(pk=product_id)
        versions = product.get_versions()  # Получаем все версии продукта
        context = {
            'product': product,
            'versions': versions,  # Передаем версии продукта в контекст
        }
        return render(request, 'product_list.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('goods:index')

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = ['goods.can_unpublish_product', 'goods.can_change_product_description', 'goods.can_change_product_category']

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

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
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    successful_url = reverse_lazy('goods:contacts')

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации


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
