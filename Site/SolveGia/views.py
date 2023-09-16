from django.shortcuts import render, redirect, get_object_or_404, Http404, reverse
from django.http import HttpRequest

from multiprocessing import Process
import random
from math import ceil
import time

from .models import *


def get_task_closets_to_difficulty(type_number, difficulty, category):
    mini = Task.objects.filter(type_number=type_number, category=category).order_by('rating').first().rating
    changed_diff = difficulty if difficulty > mini else mini
    tasks_of_type_number_ordered: list[Task] = list(
        Task.objects.filter(
            type_number=type_number,
            rating__lte=changed_diff).order_by('-rating').values_list('pk', 'rating'))

    maxi = tasks_of_type_number_ordered[0][1]
    tasks = []
    for task in tasks_of_type_number_ordered:
        if task[1] == maxi:
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
            answers = request.POST.get('answers')

            if not answers:
                answers = 'off'

            if difficulty == '':
                difficulty = random.randint(1, 100)

            return redirect(
                'gen-r-var',
                cat_name=category.name,
                difficulty=difficulty,
                answers=answers)
        
        elif action == 'show-vars':
            category = get_object_or_404(Category, name=request.POST.get('category[]'))

            return redirect(
                'show-vars',
                cat_name=category.name,
                page=0)

    return render(request, template_name='SolveGia/index.html', context=context)


def generate_random_variant(request: HttpRequest, cat_name, difficulty, answers):
    st = time.time()
    try:
        difficulty = int(difficulty)
    except TypeError:
        raise Http404

    if not (0 <= difficulty <= 100):
        raise Http404
    
    category = get_object_or_404(Category, name=cat_name)
    
    if answers == 'off':
        answers = False
    elif answers == 'on':
        answers = True
    else:
        raise Http404

    context = {
        'title': 'Random variant',
        'tasks': [],
        'answers': answers,
    }

    for i in range(1, 26):
        context['tasks'].append(get_task_closets_to_difficulty(i, difficulty, category=category))

    def new_var_process(Variant, tasks):
        new_var = Variant(category=category)
        new_var.save()
        new_var.tasks.set(tasks)
        new_var.save()
    
    new_var_p = Process(target=new_var_process, args=(Variant, context['tasks']))
    new_var_p.start()
    context['time'] = time.time() - st
    return render(request, template_name='SolveGia/show-variant.html', context=context)


def show_vars(request, cat_name, page=0):
    category = get_object_or_404(Category, name=cat_name)
    
    if page < 0:
        raise Http404
    
    variants = list(Variant.objects.filter(category=category)[page * 19:(page + 1) * 19])

    context = {
        'title': f'All variants of {category.name} - p{page}',
        'variants': variants,
        'category': category,
    }

    return render(request, template_name='SolveGia/show-vars.html', context=context)


def show_variant(request, cat_name, var_id, answers):
    st = time.time()
    category = get_object_or_404(Category, name=cat_name)
    
    if answers == 'off':
        answers = False
    elif answers == 'on':
        answers = True
    else:
        raise Http404
    
    variant = get_object_or_404(Variant, pk=var_id, category=category)

    context = {
        'title': f'Variants of {category.name} - №{variant.pk}',
        'tasks': list(variant.tasks.all()),
        'variant': variant,
        'answers': answers,
    }
    context['time'] = time.time() - st
    return render(request, template_name='SolveGia/show-variant.html', context=context)


def show_task(request, cat_name, task_id):
    category = get_object_or_404(Category, name=cat_name)
    task = get_object_or_404(Task, category=category, pk=task_id)

    context = {
        'title': f'Task №{task.type_number}{task.pk} of {category.name}',
        'task': task,
    }

    return render(request, template_name='SolveGia/show-task.html', context=context)