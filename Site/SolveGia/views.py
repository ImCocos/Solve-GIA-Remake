from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http import HttpRequest, HttpResponseNotFound

import random

from .models import *


def get_task_closets_to_difficulty(type_number, difficulty, category):
    mini = Task.objects.filter(type_number=type_number, category=category).order_by('rating').first().rating
    changed_diff = difficulty if difficulty > mini else mini
    tasks_of_type_number_ordered: list[Task] = list(
        Task.objects.filter(
            type_number=type_number,
            rating__lte=changed_diff).order_by('-rating').values_list('pk', 'rating'))

    max_rating = tasks_of_type_number_ordered[0][1]
    tasks = []
    for task in tasks_of_type_number_ordered:
        if task[1] == max_rating:
            tasks.append(task)
    return Task.objects.get(pk=random.choice(tasks)[0])


def index(request: HttpRequest):
    categories = list(Category.objects.all())
    context = {
        'title': 'Main page',
        'categories': categories,
    }

    if request.method == 'POST':
        action = request.POST.get('SUBMIT')

        if action == 'gen':
            category = get_object_or_404(Category, name=request.POST.get('category[]'))
            difficulty = request.POST.get('difficulty[]')

            if difficulty == '':
                difficulty = random.randint(1, 100)

            return redirect(
                'gen-r-var',
                cat_name=category.name,
                difficulty=difficulty)

    return render(request, template_name='SolveGia/index.html', context=context)


def generate_random_variant(request: HttpRequest, cat_name, difficulty):
    try:
        difficulty = int(difficulty)
    except TypeError:
        return HttpResponseNotFound('404 - Not found!', status=404)

    if not (0 <= difficulty <= 100):
        return HttpResponseNotFound('404 - Not found!', status=404)
    
    if not Category.objects.filter(name=cat_name).exists():
        return HttpResponseNotFound('404 - Not found!', status=404)

    category = Category.objects.get(name=cat_name)

    context = {
        'title': 'Random variant',
    }

    context['tasks'] = []

    for i in range(1, 26):
        context['tasks'].append(get_task_closets_to_difficulty(i, difficulty, category=category))

    return render(request, template_name='SolveGia/show_variant.html', context=context)
