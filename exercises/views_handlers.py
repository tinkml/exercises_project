from django.db.models import Min, Max
from .models import Task
from random import randint


def create_tasks_unique_url(request, vars_list, task, category_url, level):
    vars_str = '_'.join(str(i) for i in vars_list)
    meta = request.META.get("HTTP_REFERER").split('/')
    url = f'{meta[0]}//{meta[2]}/{category_url}/{level}/{task.url}/{vars_str}'
    return url


def get_task_id_range(url_of_category):
    min_id = Task.objects.filter(category__url=url_of_category).aggregate(Min('id'))['id__min']
    max_id = Task.objects.filter(category__url=url_of_category).aggregate(Max('id'))['id__max']
    return min_id, max_id


def increasing_difficulty_level(passed_tasks):
    passed_tasks += 1
    if passed_tasks // 5 >= 10:
        next_level = 10
    elif passed_tasks <= 5:
        next_level = 1
    else:
        next_level = passed_tasks // 5 + 1
    return next_level, passed_tasks


def get_level_and_category_url(request):
    url_of_category = request.POST.get('categories')
    chosen_level = int(request.POST.get('level'))
    return url_of_category, chosen_level


def get_random_task(category_url):
    min_id, max_id = get_task_id_range(category_url)
    random_id = randint(min_id, max_id)
    task = Task.objects.filter(category__url=category_url).get(id=random_id)
    return task


def create_error_data(request, category_url):
    description = request.POST.get('description')
    correct_answer = request.POST.get('correct_answer')
    category_name = request.POST.get('category_name')
    level = request.POST.get('level')
    solved_tasks = request.POST.get('solved')
    unique_url = request.POST.get('unique_url')
    error = 'Your answer is not correct. Don''t worry and try again!'
    data = {
        'description': description,
        'level': level,
        'solved': solved_tasks or 0,
        'correct_answer': correct_answer,
        'category_name':category_name,
        'category_url': category_url,
        'unique_url': unique_url,
        'error': error}
    return data
