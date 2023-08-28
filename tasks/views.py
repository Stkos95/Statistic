from django.http import HttpRequest, HttpResponse, Http404
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.dates import DateMixin, BaseDateListView, ArchiveIndexView

from .models import Task, Category
from django.views.generic import DetailView
from .forms import AddTaskForm
import datetime

from django.views.generic.list import ListView

menu = [{'name': "Schedule", 'link': '#'},
        {'name': 'About', 'link': '#'}]


def schedule_redirect(request):
    return redirect('schedule_category', slug='all')


def schedule(request, category_slug, date=None):
    all_categories = Category.objects.all()
    all_tasks = Task.objects.all()
    if category_slug == 'empty':
        all_tasks = all_tasks.filter(category__isnull=True)

    elif category_slug != 'empty' and category_slug != 'all':

        all_tasks = all_tasks.filter(category__slug=category_slug)

    if date:
        d = '-'.join(date.split('-')[::-1])
        all_tasks = all_tasks.filter(deadline__date=date)

    return render(request, 'tasks/schedule.html', {'tasks': all_tasks,
                                                   'section': 'schedule',
                                                   'all_categories': all_categories,
                                                   'category_slug': category_slug})


def about(request):
    return render(request, 'tasks/about.html', {'section': 'about'})


def task_detail(request, task_id):
    current_task = get_object_or_404(Task, id=task_id)
    print(current_task.name)
    return render(request, 'tasks/detail.html', {'task': current_task})

def create_task(request, category_slug):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('schedule_category', category_slug=category_slug)
    try:
        cur_category = get_object_or_404(Category, slug=category_slug)
    except Http404:
        cur_category = ''
    now = datetime.datetime.now()
    form = AddTaskForm(data={'category': cur_category,
                             })
    # form = TestForm()
    return render(request, 'tasks/create.html', {'form': form,
                                                 'category': category_slug})



class Test(ArchiveIndexView):
    date_field = 'deadline'
    model = Task
    allow_future = True
    template_name = 'tasks/schedule.html'
    date_list_period = 'day'
    context_object_name = 'tasks'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_slug'] = self.kwargs['slug']
        context['all_categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        all_tasks = Task.objects.all()
        cs = self.kwargs['slug']
        if cs == 'empty':
            all_tasks = all_tasks.filter(category__isnull=True)

        elif cs != 'empty' and cs != 'all':

            all_tasks = all_tasks.filter(category__slug=cs)
        date = self.kwargs.get('date', None)
        if date:
            print(date)
            all_tasks.filter(deadline=date)
            print(all_tasks)
            print('hello')

        return all_tasks






