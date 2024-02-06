Задание 1
Создайте новое приложение для работы с пользователем. Определите собственную форму для пользователя, при этом задайте электронную почту как поле для авторизации.

Также добавьте поля:

«Аватар»,
«Номер телефона»,
«Страна».
Задание 2
В сервисе реализуйте функционал аутентификации, а именно:

регистрацию пользователя по почте и паролю;
верификацию почты пользователя через отправленное письмо;
авторизацию пользователя;
восстановление пользователя на автоматически сгенерированный пароль.
Задание 3
Закройте для анонимных пользователей все контроллеры, которые отвечают за работу с продуктами. При этом создаваемые продукты должны автоматически привязываться к авторизованному пользователю.

Не забудьте добавить поле для продуктов, через которое пользователь будет привязываться. Текущий авторизованный пользователь доступен в любом контроллере через 
self.request.user
.

Для закрытия контроллеров, отвечающих за работу с продуктами, для анонимных пользователей и автоматического привязывания создаваемых продуктов к авторизованному пользователю, вам потребуется использовать Django's LoginRequiredMixin и переопределить метод form_valid в ProductCreateView и ProductUpdateView.

Вот обновленный код с необходимыми изменениями:

from django.contrib.auth.mixins import LoginRequiredMixin

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('goods:index')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем создаваемый продукт к авторизованному пользователю
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

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
В обновленном коде мы импортировали LoginRequiredMixin из django.contrib.auth.mixins и добавили его в качестве базового класса для ProductCreateView и ProductUpdateView. Это требует, чтобы пользователь был аутентифицирован, чтобы получить доступ к этим контроллерам.

Мы также переопределили метод form_valid в ProductCreateView, чтобы установить поле user создаваемого продукта равным текущему авторизованному пользователю (self.request.user).

Теперь только авторизованные пользователи смогут получить доступ к созданию и обновлению продуктов, и создаваемые продукты будут автоматически привязаны к авторизованному пользователю.