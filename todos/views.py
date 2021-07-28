from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Task, Category


class TaskListView(LoginRequiredMixin, ListView):
    """
    نمایش لیست تسک ها

    :model: مدلی/جدول دیتابیس که جزییات تسک از فیلدهای آن خوانده می شود
    :template_name: صفحه ای که این ویو در آن رندر می شود
    """
    model = Task
    template_name = 'tasks/task_list.html'


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
    template_name = 'tasks/new_task.html'
    fields = ('title', 'description', 'category', 'priority', 'deadline')

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
    fields = ('title', 'description', 'category', 'priority', 'deadline')
    template_name = 'tasks/task_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


# category views

class CategoryListView(LoginRequiredMixin, ListView):
    """
    نمایش لیست دسته بندی تسک ها

    :model: مدل/جدول دیتابیس شامل دسته بندی ها
    :template_name: صفحه ای که این ویو در آن رندر می شود
    """
    model = Category
    template_name = 'tasks/category_list.html'


class CategoryTasksListView(LoginRequiredMixin, ListView):
    """
    نمایش لیست تسکهای هر دسته بندی

    :model: مدل/جدول دیتابیس شامل دسته بندی ها
    :template_name: صفحه ای که این ویو در آن رندر می شود
    """
    model = Category
    template_name = 'tasks/category_detail_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['category_tasks_list'] = Task.objects.all()
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'tasks/new_ctg.html'
    fields = ('name',)


class DeleteCategoryView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    ویوی حذف دسته بندی انتخابی را ایجاد می کند

    :model: مدل/جدول مرجع
    :template_name: صفحه ای که این ویو در آن رندر می شود
    :success_url: آدرس صفحه ای که بعد موفق بودن حذف کاربر به آن منتقل می شود
    """
    model = Task
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
    model = Task
    fields = ('name',)
    template_name = 'tasks/ctg_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
