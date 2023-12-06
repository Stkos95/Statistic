from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from django.http import HttpResponseForbidden
from django.http import HttpRequest, HttpResponse, Http404
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.dates import DateMixin, BaseDateListView, ArchiveIndexView
from django.contrib.auth.views import LoginView, LogoutView
import logging
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

from .models import Task, Category
from django.views.generic import DetailView, CreateView, FormView
from .forms import AddTaskForm
import datetime
import logging

from django.views.generic.list import ListView

logging.basicConfig(level=logging.DEBUG)

menu = [{'name': "Schedule", 'link': '#'},
        {'name': 'About', 'link': '#'}]

logger = logging.getLogger(__name__)




def schedule_redirect(request: HttpRequest):
    return redirect('tasks:schedule_category', slug='all')


def about(request):
    return render(request, 'tasks/about.html', {'section': 'about'})


class TaskDetail(DetailView):
    template_name = 'tasks/detail.html'
    model = Task
    context_object_name = 'task'


class CreateTask(CreateView):
    model = Task
    form_class = AddTaskForm
    template_name = 'tasks/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('slug')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




def home(request):
    if request.user.is_authenticated:
        view = Test1.as_view()
        return view(request)
    else:
        return render(request, 'tasks/home.html')


class Test1(View):
    def get(self, request):
        return HttpResponse('А теперь вы авторизованы! :)')


class Test(ListView):
    # login_url = 'login'
    # date_field = 'deadline'
    model = Task
    # allow_future = True
    template_name = 'tasks/schedule.html'
    # date_list_period = 'day'
    context_object_name = 'tasks'
    allow_empty = True

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_slug'] = self.kwargs['slug']
        context['all_categories'] = Category.objects.all()

        return context


    def get_queryset(self):
        if self.request.user.is_authenticated:
            print('hello')
            all_tasks = Task.objects.filter(user=self.request.user)

            category_slug = self.kwargs['slug']

            if category_slug == 'empty':
                all_tasks = all_tasks.filter(category__isnull=True)

            elif category_slug != 'empty' and category_slug != 'all':

                all_tasks = all_tasks.filter(category__slug=category_slug)
            date = self.kwargs.get('date', None)
            if date:
                all_tasks = all_tasks.filter(deadline__date=date)

        else:
            all_tasks = Task.objects.all()
            print('world')

        return all_tasks


class MyLoginView(LoginView):
    next_page = 'tasks:schedule'



class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registration.html'
    success_url = '/'

    def form_invalid(self, form):
        return super().form_invalid(form)



