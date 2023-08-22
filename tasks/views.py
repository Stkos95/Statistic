from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Task, Category

menu = [{'name': "Schedule", 'link': '#'},
        {'name': 'About', 'link': '#'}]


def schedule(request, date=None, category_slug=None):
    all_categories = Category.objects.all()
    all_tasks = Task.objects.all()
    if category_slug == 'empty':
        all_tasks = all_tasks.filter(category__isnull=True)

    elif category_slug:
        all_tasks = all_tasks.filter(category__slug=category_slug)

    if date:
        d = '-'.join(date.split('-')[::-1])
        all_tasks = all_tasks.filter(deadline__date=d)



    return render(request, 'tasks/schedule.html', {'tasks': all_tasks,
                                                   'menu': menu,
                                                   'section': 'schedule',
                                                   'all_categories': all_categories,
                                                   'category_slug': category_slug})


def about(request):
    return render(request, 'tasks/about.html', {'section': 'about'})


def task_detail(request, task_id):
    current_task = get_object_or_404(Task, id=task_id)
    print(current_task.name)
    return render(request, 'tasks/detail.html', {'task': current_task})
