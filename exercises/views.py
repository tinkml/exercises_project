import pyperclip
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .models import Category, UsersCategoryLevel
from .task_handlers import *
from .views_handlers import *

functions = {
    'numbers_conversion': {
        'create_task': create_numbers_conversion_task,
        'get_answer': get_numbers_conversion_answer},

    'bit_arithmetic': {
        'create_task': create_bit_arithmetic_task,
        'get_answer': get_bit_arithmetic_answer},

    'arithmetic_logic': {
        'create_task': create_arithmetic_logic_task,
        'get_answer': get_arithmetic_logic_answer},

    'the_powers_of_two': {
        'create_task': create_the_powers_of_two_task,
        'get_answer': get_the_powers_of_two_answer},

    'twos_complement_arithmetic': {
        'create_task': create_twos_complement_arithmetic_task,
        'get_answer': get_twos_complement_arithmetic_answer},

    'big_and_little_endian_byte_order': {
        'create_task': create_big_and_little_endian_byte_order_task,
        'get_answer': get_big_and_little_endian_byte_order_answer},

    'pointer_arithmetic': {
        'create_task': create_pointer_arithmetic_task,
        'get_answer': get_pointer_arithmetic_answer},

    'bytes_conversion': {
        'create_task': create_bytes_conversion_task,
        'get_answer': get_bytes_conversion_answer},

    'ipv4_subnet_mask': {
        'create_task': create_ipv4_subnet_mask_task,
        'get_answer': get_ipv4_subnet_mask_answer},

    'ieee_754_floats': {
        'create_task': create_ieee_754_floats_task,
        'get_answer': get_ieee_754_floats_answer},

    'numeric_limits': {
        'create_task': create_numeric_limits_task,
        'get_answer': get_numeric_limits_answer},
}


def log_out_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/categories')


def show_home_page(request):
    return render(request, 'exercises/home_page.html')


def show_categories(request):
    categories = Category.objects.all()
    levels = range(1, 11)
    return render(request, 'exercises/categories.html', {'categories': categories, 'levels': levels})


answer = ''
category_url = ''
data = {}
description = ''
level = None or 1
solved_tasks = 0
unique_url = ''
CATEGORY = ''
USER = ''


def show_task_from_url(request, category, lvl, task_url, vars_str):
    global answer, category_url, description, level, solved_tasks

    category_url = category
    level = int(lvl)
    data = {
        'description': description,
        'level': level,
        'solved': solved_tasks}

    if request.POST.get('get_answer'):
        data['answer'] = f'Answer: {answer}'
        return render(request, 'exercises/task.html', context=data)

    user_answer = request.POST.get('answer')
    if user_answer:
        if user_answer == str(answer):
            solved_tasks += 1
            return redirect('/task')
        else:
            data['error'] = 'Your answer is not correct. Don''t worry and try again!'

    vars_list = vars_str.split('_') if '_' in vars_str else [vars_str]
    if description == '' and answer == '':
        description = Task.objects.get(url=task_url).description.format(*vars_list)
        answer = functions[category_url]['get_answer'](task_url, vars_list)

    return render(request, 'exercises/task.html', context=data)


def get_task(request):
    global answer, CATEGORY, category_url, data, description, level, solved_tasks, unique_url, USER

    if request.POST.get('return'):
        answer = category_url = description = unique_url = ''
        level = 1
        solved_tasks = 0
        return redirect('/categories')

    if request.POST.get('copy'):
        pyperclip.copy(unique_url)
        return render(request, 'exercises/task.html', context=data)

    if request.POST.get('get_answer'):
        data['answer'] = f'Answer: {answer}'
        return render(request, 'exercises/task.html', context=data)

    user_answer = request.POST.get('answer')
    if user_answer:
        if user_answer == answer:
            if request.user.is_authenticated:
                user_category_level = UsersCategoryLevel.objects.filter(user=USER, category=CATEGORY).get()
                user_category_level.solved_tasks += 1
                solved_tasks = user_category_level.solved_tasks
                user_category_level.save()
                level, solved_tasks = increasing_difficulty_level(solved_tasks)
            else:
                level, solved_tasks = increasing_difficulty_level(solved_tasks)
        else:
            data['error'] = 'Your answer is not correct. Don''t worry and try again!'
            print(data)
            return render(request, 'exercises/task.html', context=data)

    if user_answer is None and request.method == 'POST':
        category_url = request.POST.get('categories')
        if request.user.is_authenticated:
            USER = User.objects.get(id=request.user.id)
            CATEGORY = Category.objects.get(url=category_url)
            object_in_bd = UsersCategoryLevel.objects.filter(user=USER, category=CATEGORY).exists()
            if not object_in_bd:
                user_category_level = UsersCategoryLevel()
                user_category_level.user = USER
                user_category_level.category = CATEGORY
                user_category_level.solved_tasks = 0
                user_category_level.save()
            else:
                user_category_level = UsersCategoryLevel.objects.filter(user=USER, category=CATEGORY).get()
                solved_tasks = user_category_level.solved_tasks
                level, solved_tasks = increasing_difficulty_level(solved_tasks)
        else:
            level = int(request.POST.get('level'))

    task = get_random_task(category_url)
    new_tasks_handler = functions[category_url]['create_task']
    description, answer, vars_list = new_tasks_handler(task, level)
    unique_url = create_tasks_unique_url(request, vars_list, task, category_url, level)

    data = {
        'description': description,
        'level': level,
        'solved': solved_tasks}

    return render(request, 'exercises/task.html', context=data)
