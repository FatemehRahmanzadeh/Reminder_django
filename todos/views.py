from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .forms import CreateTask
from .models import Task, Category


class TaskListView(LoginRequiredMixin, ListView):
    """
    نمایش لیست تسک ها

    :model: مدلی/جدول دیتابیس که جزییات تسک از فیلدهای آن خوانده می شود
    :template_name: صفحه ای که این ویو در آن رندر می شود
    """
    model = Task
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).exclude(deadline__lt=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        try:
            context['ex_tasks'] = Task.objects.get_ex_tasks().filter(user=self.request.user)
        except Task.DoesNotExist:
            context['ex_tasks'] = None
        return context

    # def tasks_as_json(self):
    #     #     dictionaries = [obj.as_dict() for obj in self.get_queryset()]
    #     #     return HttpResponse(json.dumps({"tasks": dictionaries}), content_type='application/json')

    # def get_tasks(self, request, *args, **kwargs):
    #     qs = Task.objects.all()
    #     data = serialize("json", qs)
    #     return JsonResponse(data, safe=False)


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    نمایش جزییات هرتسک

    :model: مدلی/جدول دیتابیس که جزییات تسک از فیلدهای آن خوانده می شود
    :template_name: صفحه ای که این ویو در آن رندر می شود
    """
    model = Task
    template_name = 'tasks/task_detail.html'


class DeleteTaskView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    ویوی حذف تسک انتخابی را ایجاد می کند

    :model:مدل/جدول مرجع
    :template_name: صفحه ای که این ویو در آن رندر می شود
    :success_url: آدرس صفحه ای که بعد موفق بودن حذف کاربر به آن منتقل می شود
    """
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    ایجاد تسک جدید

    :model: مدل/جدول تسک در دیتابیس
    :template_name: صفحه ای که این ویو در آن رندر می شود
    :fields: فیلدهای موجود در فرم ایجاد تسک
    """
    model = Task
    form_class = CreateTask
    template_name = 'tasks/new_task.html'

    # fields = ('title', 'description', 'category', 'status', 'priority', 'deadline')

    def get_form(self, form_class=CreateTask):
        """
        هر کاربر حق داره فقط دسته بندی هایی که خودش تعریف کرده ببینه و انتخاب کنه
        :param form_class: اگر فرم کاستوم تعریف شده بود
        :return: فرم با دسته بندی شخصی سازی شده
        """
        form = super(TaskCreateView, self).get_form(form_class)
        form.fields["category"].queryset = self.request.user.user_categories.all()
        return form

    def form_valid(self, form):
        """
        اتوماتیک یوزر فعال به عنوان صاحب تسک انتخاب شود
        :param form: فرمی که با آن تسک ایجاد می شود
        :return: خروجی متد والد تغییریافته :
        HttpResponseRedirect(self.get_success_url())
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    ویوی ویرایش تسک انتخابی را ایجاد می کند

    :model: مدل/جدول مرجع
    :template_name: صفحه ای که این ویو در آن رندر می شود
    :fields: فیلدهای قابل ویرایش (منطقی نیست که کاربر آن برای ویرایش در دسترس باشد.)
    """
    model = Task
    fields = ('title', 'description', 'category', 'status', 'priority', 'deadline')
    template_name = 'tasks/task_edit.html'

    def get_form(self, form_class=None):
        """
        هر کاربر حق داره فقط دسته بندی هایی که خودش تعریف کرده ببینه و انتخاب کنه
        :param form_class: اگر فرم کاستوم تعریف شده بود
        :return: فرم با دسته بندی شخصی سازی شده
        """
        form = super(TaskUpdateView, self).get_form(form_class)
        form.fields["category"].queryset = self.request.user.user_categories.all()
        return form

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


# category views

class CategoryListView(LoginRequiredMixin, ListView):
    """
    نمایش لیست دسته بندی تسک ها

    :model: مدل/جدول دیتابیس شامل دسته بندی ها
    :template_name: صفحه ای که این ویو در آن رندر می شود
    """
    model = Category
    template_name = 'tasks/category_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).exclude(cat_tasks__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        try:
            context['empty_categories'] = Category.objects.empty_categories().filter(user=self.request.user)
        except Category.DoesNotExist:
            context['empty_categories'] = None
        return context


class CategoryTasksListView(LoginRequiredMixin, ListView):
    """
    نمایش لیست تسکهای هر دسته بندی

    :model: مدل/جدول دیتابیس شامل دسته بندی ها
    :template_name: صفحه ای که این ویو در آن رندر می شود
    """
    model = Category
    template_name = 'tasks/category_detail_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        try:
            context['done'] = Task.objects.get_done_tasks()['done'].filter(category__id=pk)
            context['due'] = Task.objects.get_done_tasks()['due'].filter(category__id=pk)
            context['category_name'] = Category.objects.get(pk=pk)
        except Task.DoesNotExist:
            context['done'] = None
            context['due'] = None
            context['category_name'] = None
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'tasks/new_ctg.html'
    fields = ('name',)

    def form_valid(self, form):
        """
        اتوماتیک یوزر فعال به عنوان صاحب دسته بندی انتخاب شود
        :param form: فرمی که با آن دسته بندی ایجاد می شود
        :return: خروجی متد والد تغییریافته :
        HttpResponseRedirect(self.get_success_url())
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteCategoryView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    ویوی حذف دسته بندی انتخابی را ایجاد می کند

    :model: مدل/جدول مرجع
    :template_name: صفحه ای که این ویو در آن رندر می شود
    :success_url: آدرس صفحه ای که بعد موفق بودن حذف کاربر به آن منتقل می شود
    """
    model = Category
    template_name = 'tasks/ctg_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    ویوی ویرایش دسته بندی انتخابی را ایجاد می کند

    :model: مدل/جدول مرجع
    :template_name: صفحه ای که این ویو در آن رندر می شود
    :fields: فیلدهای قابل ویرایش
    """
    model = Category
    fields = ('name',)
    template_name = 'tasks/ctg_edit.html'
    success_url = reverse_lazy('categories')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
