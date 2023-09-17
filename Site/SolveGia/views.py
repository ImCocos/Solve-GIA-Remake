from django.shortcuts import render, redirect, get_object_or_404, Http404, reverse
from django.http import HttpRequest

from multiprocessing import Process
import random
from math import ceil
import time

from .models import Task, Category, Variant, Attempt, TypeNumber, Result, Homework, CustomGroup


def get_task_closets_to_difficulty(type_number, difficulty, Category: Category):
    type_number_query = Category.type_numbers.get(number=type_number)
    mini = type_number_query.tasks.all().order_by('rating').first().rating
    changed_diff = difficulty if difficulty > mini else mini   
    tasks_of_type_number_ordered = type_number_query.tasks.all().filter(rating__lte=changed_diff).order_by('-rating')

    maxi = tasks_of_type_number_ordered.first().rating
    tasks = list(tasks_of_type_number_ordered.filter(rating=maxi))

    return random.choice(tasks)


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
    tns = category.get_str_tns_for_infa()
    rating_sum = 0
    tasks = []
    for i in range(1, category.amount_of_type_numbers + 1):
        context['tasks'].append((get_task_closets_to_difficulty(i, difficulty, category), tns[i-1]))
        rating_sum += context['tasks'][i-1][0].rating
        tasks.append(context['tasks'][i-1][0])

    new_var = Variant(category=category, median_rating=rating_sum // category.amount_of_type_numbers)
    new_var.save()
    new_var.tasks.set(tasks)
    new_var.save()

    context['time'] = time.time() - st
    if answers:
        return render(request, template_name='SolveGia/show-variant.html', context=context)
    else:
        return redirect('solve-variant', cat_name=cat_name, var_id=new_var.pk)


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
    tasks = list(variant.tasks.all())
    tns = category.get_str_tns_for_infa()
    context = {
        'title': f'Variant №{variant.pk}({variant.median_rating})',
        'tasks': [(tasks[i-1], tns[i-1]) for i in range(1, category.amount_of_type_numbers + 1)],
        'variant': variant,
        'answers': answers,
    }
    context['time'] = time.time() - st
    return render(request, template_name='SolveGia/show-variant.html', context=context)


def show_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    context = {
        'title': f'Task №{task.pk}',
        'task': task,
    }

    return render(request, template_name='SolveGia/show-task.html', context=context)


def solve_variant(request: HttpRequest, cat_name, var_id, task_number=1):
    category = get_object_or_404(Category, name=cat_name)
    variant = get_object_or_404(Variant, pk=var_id)
    if task_number > category.amount_of_type_numbers:
        raise Http404 

    context = {
        'title': f'Variant №{variant.pk}({variant.median_rating})',
        'task': (variant.tasks.all()[task_number - 1], category.get_str_tns_for_infa()[task_number - 1]),
    }

    if request.method == 'POST':
        answer = request.POST.get('answer')
        time = int(request.COOKIES['time'])

        """
        Мега умная формула которая считает сложность В ПРОЦЕНТАХ...
        Потом сохраняем сложность в бд.
        """

        if task_number < category.amount_of_type_numbers:
            red = redirect('solve-variant', cat_name=cat_name, var_id=var_id, task_number=task_number + 1)
            red.set_cookie('time', '0')
            return red

        return redirect('home')

    return render(request, template_name='SolveGia/solve-variant.html', context=context)
