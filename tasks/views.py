from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import CustomUserCreationForm

from django.http import HttpRequest, HttpResponse, Http404
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.dates import DateMixin, BaseDateListView, ArchiveIndexView
from django.contrib.auth.views import LoginView, LogoutView
import logging
from django.contrib.auth.mixins import LoginRequiredMixin


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
    logger.warning('REDIRECTION')
    return redirect('schedule_category', slug='all')


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_slug'] = self.kwargs['slug']
        context['all_categories'] = Category.objects.all()
        print(context)

        return context


    def get_queryset(self):

        all_tasks = Task.objects.filter(user=self.request.user)
        logger.debug(f'{all_tasks=}')
        cs = self.kwargs['slug']
        logger.debug(f'{cs=}')
        if cs == 'empty':
            all_tasks = all_tasks.filter(category__isnull=True)

        elif cs != 'empty' and cs != 'all':

            all_tasks = all_tasks.filter(category__slug=cs)
        date = self.kwargs.get('date', None)
        if date:
            all_tasks = all_tasks.filter(deadline__date=date)
        logger.debug(f'{all_tasks}')
        return all_tasks


class MyLoginView(LoginView):
    pass



class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registration.html'
    success_url = '/'

    def form_invalid(self, form):
        print(f'{form.errors=}')
        return super().form_invalid(form)





