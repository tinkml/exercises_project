from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .models import Category, UsersCategoryLevel
from .task_handlers import *
from .views_handlers import *
import logging

user_log = logging.getLogger('user_log')
views_log = logging.getLogger('views_log')

file_handler = logging.FileHandler(filename='logs/user_flow.log', encoding='utf8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
user_log.addHandler(file_handler)
file_handler.setLevel(logging.DEBUG)
user_log.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename='logs/views.log', encoding='utf8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
views_log.addHandler(handler)
handler.setLevel(logging.DEBUG)
views_log.setLevel(logging.DEBUG)

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
        user_log.debug(f'[USER_ID] {request.user.id} ----- [LOGOUT]')
        logout(request)
        return redirect('/categories')


def show_home_page(request):
    user_log.debug(f'[USER_ID] {request.user.id} ----- [HOME_PAGE]')
    return render(request, 'exercises/home_page.html')


def show_categories(request):
    user_log.debug(f'[USER_ID] {request.user.id} ----- [CATEGORIES]')
    categories = Category.objects.all().order_by('id')
    return render(request, 'exercises/categories.html', {'categories': categories})


def show_task_from_url(request, category, lvl, task_url, vars_str):
    user_log.debug(f'[USER_ID] {request.user.id} ----- [TASK_FROM_URL]')
    category_url = category
    level = int(lvl)

    user_answer = request.POST.get('answer')
    if user_answer:
        correct_answer = request.POST.get('correct_answer')
        user_log.info(f'[USER_ID] {request.user.id} ----- [USER_ANSWER] {user_answer}')
        user_log.info(f'[USER_ID] {request.user.id} ----- [CORRECT_ANSWER] {correct_answer}')
        if user_answer == correct_answer:
            user_log.debug(f'[USER_ID] {request.user.id} ----- [SOLVED_TASK_FROM_URL]')
            return redirect('/categories')
        else:
            user_log.debug(f'[USER_ID] {request.user.id} ----- [DID_NOT_SOLVE_TASK_FROM_URL]')
            data = create_error_data(request, category_url)
            return render(request, 'exercises/task.html', context=data)

    vars_list = vars_str.split('_') if '_' in vars_str else [vars_str]
    description = Task.objects.get(url=task_url).description.format(*vars_list)
    correct_answer = functions[category_url]['get_answer'](task_url, vars_list)

    data = {
        'description': description,
        'level': level,
        'solved': '0',
        'correct_answer': correct_answer,
        'category_url': category_url}

    return render(request, 'exercises/task.html', context=data)


def get_task(request):

    if request.POST.get('return'):
        user_log.debug(f'[USER_ID] {request.user.id} ----- [RETURN]')
        return redirect('/categories')

    user_answer = request.POST.get('answer')
    user_log.debug(f'[METHOD] {request.method}')
    if user_answer is None and request.method == 'POST':
        category_url = request.POST.get('category')
        views_log.debug(f'\n[CATEGORY] {category_url}\n')
        user_log.info(f'[USER_ID] {request.user.id} ----- [CATEGORY] {category_url}')
        if request.user.is_authenticated:
            user_log.debug(f'[USER_ID] {request.user.id} ----- [USER_IS_AUTHENTICATED]')
            USER = User.objects.get(id=request.user.id)
            CATEGORY = Category.objects.get(url=category_url)
            object_in_bd = UsersCategoryLevel.objects.filter(user=USER, category=CATEGORY).exists()
            if not object_in_bd:
                user_log.debug(f'[USER_ID] {request.user.id} ----- [CREATE_OBJECT_IN_BD]')
                user_category_level = UsersCategoryLevel()
                user_category_level.user = USER
                user_category_level.category = CATEGORY
                user_category_level.solved_tasks = 0
                user_category_level.save()
                solved_tasks = 0
                level = int(request.POST.get('level'))
                user_log.info(f'[USER_ID] {request.user.id} ----- [LEVEL] {level} [SOLVED] {solved_tasks}')
            else:
                user_log.debug(f'[USER_ID] {request.user.id} ----- [ALREADY_HAS_OBJECT_IN_BD]')
                user_category_level = UsersCategoryLevel.objects.filter(user=USER, category=CATEGORY).get()
                solved_tasks = user_category_level.solved_tasks
                level, solved_tasks = increasing_difficulty_level(solved_tasks)
                user_log.info(f'[USER_ID] {request.user.id} ----- [LEVEL] {level} [SOLVED] {solved_tasks}')
        else:
            user_log.debug(f'[USER_ID] {request.user.id} ----- [USER_IS_NOT_AUTHENTICATED]')
            solved_tasks = 0
            level = int(request.POST.get('emojis_level')) + 1
            user_log.info(f'[USER_ID] {request.user.id} ----- [LEVEL] {level} [SOLVED] {solved_tasks}')

    if user_answer:
        correct_answer = request.POST.get('correct_answer')
        category_url = request.POST.get('category_url')
        user_log.info(f'[USER_ID] {request.user.id} ----- [USER_ANSWER] {user_answer}')
        user_log.info(f'[USER_ID] {request.user.id} ----- [CORRECT_ANSWER] {correct_answer}')
        if user_answer == correct_answer:
            user_log.debug(f'[USER_ID] {request.user.id} ----- [SOLVED_TASK]')
            if request.user.is_authenticated:
                USER = User.objects.get(id=request.user.id)
                CATEGORY = Category.objects.get(url=category_url)
                user_category_level = UsersCategoryLevel.objects.filter(user=USER, category=CATEGORY).get()
                user_category_level.solved_tasks += 1
                solved_tasks = user_category_level.solved_tasks
                user_category_level.save()
                level, solved_tasks = increasing_difficulty_level(solved_tasks)
                user_log.info(f'[USER_ID] {request.user.id} ----- [LEVEL] {level} [SOLVED] {solved_tasks}')
            else:
                solved_tasks = int(request.POST.get('solved'))
                level, solved_tasks = increasing_difficulty_level(solved_tasks)
                user_log.info(f'[USER_ID] {request.user.id} ----- [LEVEL] {level} [SOLVED] {solved_tasks}')
        else:
            user_log.debug(f'[USER_ID] {request.user.id} ----- [DID_NOT_SOLVED_TASK]')
            data = create_error_data(request, category_url)
            user_log.info(f'[USER_ID] {request.user.id} ----- [DATA] {data}')
            return render(request, 'exercises/task.html', context=data)

    try:
        task = get_random_task(category_url)
    except TypeError:
        return redirect('/none_task')
    views_log.debug(f'[RANDOM_TASK] {task}')
    new_tasks_handler = functions[category_url]['create_task']
    views_log.debug(f'[TASK_HANDLER] {new_tasks_handler}')
    description, correct_answer, vars_list = new_tasks_handler(task, level)
    views_log.debug(f'[DESCRIPTION] {description} [CORRECT_ANSWER] {correct_answer}')
    unique_url = create_tasks_unique_url(request, vars_list, task, category_url, level)

    data = {
        'description': description,
        'level': level,
        'solved': solved_tasks,
        'correct_answer': correct_answer,
        'category_url': category_url,
        'unique_url': unique_url}

    views_log.debug(f'[NEW_TASKS_DATA_CREATED]\n')
    return render(request, 'exercises/task.html', context=data)


def none_task(request):
    return render(request, 'exercises/none_task_error.html')
