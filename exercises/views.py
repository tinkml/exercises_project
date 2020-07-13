import pyperclip
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from .models import TasksCategory, UsersCategoryLevel
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

answer = ''
category_url = ''
data = {}
description = ''
level = None or 1
solved_tasks = 0
unique_url = ''


def sign_up_user(request):
    user_data = {'form': UserCreationForm(), 'error': ''}
    if request.method == 'GET':
        return render(request, 'exercises/sign_up.html', context=user_data)
    else:
        user_name = request.POST.get('username')
        password_1 = request.POST.get('password1')
        password_2 = request.POST.get('password2')
        if password_1 == password_2:
            try:
                user = User.objects.create_user(username=user_name, password=password_1)
                user.save()
                login(request, user)
                return show_categories(request)
            except IntegrityError:
                user_data['error'] = 'The user with this username has been already created'
                return render(request, 'exercises/sign_up.html', context=user_data)
        else:
            user_data['error'] = 'The passwords are didn''t matched'
            return render(request, 'exercises/sign_up.html', context=user_data)


def log_out_user(request):
    if request.method == 'POST':
        logout(request)
        return show_categories(request)


def log_in_user(request):
    user_data = {'form': AuthenticationForm(), 'error': ''}
    if request.method == 'GET':
        return render(request, 'exercises/log_in.html', context=user_data)
    else:
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is None:
            user_data['error'] = 'Username and password is didn''t match'
            return render(request, 'exercises/log_in.html', context=user_data)
        else:
            login(request, user)
            return show_categories(request)


def show_categories(request):
    categories = TasksCategory.objects.all()
    levels = range(1, 11)
    return render(request, 'exercises/tasks_list.html', {'categories': categories, 'levels': levels})


def show_task_from_url(request, category, lvl, task_url, vars_str):
    global answer, category_url, description, level

    category_url = category
    level = int(lvl)
    data = {
        'description': description,
        'answer': answer,
        'level': level,
        'solved': solved_tasks,
        'err': ''}

    user_answer = request.POST.get('answer')
    if user_answer:
        if user_answer == str(answer):
            return redirect('/task')
        else:
            data['err'] = 'err'

    vars_list = vars_str.split('_') if '_' in vars_str else [vars_str]
    if description == '' and answer == '':
        description = Tasks.objects.get(url=task_url).description.format(*vars_list)
        answer = functions[category_url]['get_answer'](task_url, vars_list)

    return render(request, 'exercises/task.html', context=data)


def get_task(request):
    global answer, category_url, data, description, level, solved_tasks, unique_url

    if request.POST.get('return'):
        answer = category_url = description = unique_url = ''
        level = 1
        solved_tasks = 0
        return show_categories(request)

    if request.POST.get('copy'):
        pyperclip.copy(unique_url)
        return render(request, 'exercises/task.html', context=data)

    user_answer = request.POST.get('answer')
    if user_answer:
        if user_answer == answer:
            # TODO обновить соответсвующий объект модели UsersCategoryLevel, если user авторизирован
            data['err'] = ''
            level, solved_tasks = increasing_difficulty_level(level, solved_tasks)
        else:
            data['err'] = 'err'
            return render(request, 'exercises/task.html', context=data)

    if user_answer is None and request.method == 'POST':
        category_url, level = get_level_and_category_url(request)
        user_id = request.user.id
        category_id = TasksCategory.objects.get(url=category_url).id
        print(f'===== User id = {user_id}, Category id = {category_id} =====')
        # TODO Создать объект модели UsersCategoryLevel

    task = get_random_task(category_url)
    new_tasks_handler = functions[category_url]['create_task']
    description, answer, vars_list = new_tasks_handler(task, level)
    unique_url = create_tasks_unique_url(request, vars_list, task, category_url, level)

    data = {
        'description': description,
        'answer': answer,
        'level': level,
        'solved': solved_tasks,
        'err': ''}

    return render(request, 'exercises/task.html', context=data)
