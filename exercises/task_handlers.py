from random import randint
import math


def create_numbers_conversion_task(task, level):
    var = randint(level ** 10, 256 ** level)
    if task.name == 'Number to decimal':
        vars_list = [hex(var) if var % randint(1, 5) == 0 else bin(var)]
        answer = var
    elif task.name == 'Number to hexadecimal':
        vars_list = [var if var % randint(1, 5) == 0 else bin(var)]
        answer = hex(var)
    else:
        vars_list = [var if var % randint(1, 5) == 0 else hex(var)]
        answer = bin(var)
    description = task.description.format(*vars_list)
    return description, str(answer), vars_list


def get_numbers_conversion_answer(task_url, vars_list):
    var = vars_list[0]
    if task_url == 'number_to_decimal':
        try:
            answer = int(var, 16)
        except TypeError:
            answer = int(var, 2)
    elif task_url == 'number_to_hexadecimal':
        try:
            answer = hex(var)
        except TypeError:
            answer = hex(int(var, 2))
    else:
        try:
            answer = bin(var)
        except TypeError:
            answer = bin(int(var, 16))
    return answer


def create_bit_arithmetic_task(task, level):
    x = randint(level ** 10, 256 ** level)
    y = randint(level ** 10, 256 ** level)

    if x % randint(1, 5) == 0 and level <= 5:
        _x, _y = bin(x), bin(y)
    else:
        _x, _y = x, y
    if task.url == 'x_and_y':
        answer = x & y
    elif task.url == 'x_or_y':
        answer = x | y
    elif task.url == 'not_x':
        answer = ~ x
    elif task.url == 'x_xor_y':
        answer = x ^ y
    elif task.url == 'x_right_y':
        y = _y = len(bin(x)) - 3
        answer = x >> y
    else:
        y = _y = randint(1, 10)
        answer = x << y

    vars_list = [_x, _y]
    description = task.description.format(*vars_list)
    return description, str(answer), vars_list


def get_bit_arithmetic_answer(task_url, vars_list):
    try:
        x = int(vars_list[0], 2)
        y = int(vars_list[1], 2) if len(vars_list) > 1 else None
    except TypeError:
        x = vars_list[0]
        y = vars_list[1] if len(vars_list) > 1 else None

    if task_url == 'x_and_y':
        answer = x & y
    elif task_url == 'x_or_y':
        answer = x | y
    elif task_url == 'not_x':
        answer = ~ x
    elif task_url == 'x_xor_y':
        answer = x ^ y
    elif task_url == 'x_right_y':
        answer = x >> y
    else:
        answer = x << y
    return answer


def create_arithmetic_logic_task(task, level):
    x = randint(level ** 10, 256 ** level)
    y = randint(level ** 10, 256 ** level)
    z = randint(level ** 10, 256 ** level)

    if task.url == 'expression_equal_to':
        answer = (x and y) or (x and not z)
    else:
        # TODO
        answer = (x and y) or (x and not z)

    vars_list = [x, y, x, z]
    description = task.description.format(*vars_list)
    return description, str(answer), vars_list


def get_arithmetic_logic_answer(task_url, vars_list):
    x, y, _x, z = vars_list

    if task_url == 'expression_equal_to':
        answer =(x and y) or (_x and not z)
    else:
        # TODO
        answer = (x and y) or (_x and not z)
    return answer


def create_the_powers_of_two_task(task, level):
    if task.url == 'two_x':
        var = randint(2*level, 10*level)
        answer = 2**var
    elif task.url == 'two_x_close_y':
        var = randint(level ** 10, 256 ** level)
        answer = round(math.log2(var))
    elif task.url == 'two_x_equal_bin' and level == 1:
        power = randint(2*level, 10*level)
        var = bin(2**power)
        answer = power
    elif task.url == 'two_x_equal_hex':
        power = randint(2 * level, 10 * level)
        var = hex(2 ** power)
        answer = power
    else:
        power = randint(2 * level, 10 * level)
        var = 2 ** power
        answer = power
    vars_list = [var]
    description = task.description.format(*vars_list)
    return description, str(answer), vars_list


def get_the_powers_of_two_answer(task_url, vars_list):
    var = vars_list[0]
    if task_url == 'two_x':
        answer = 2**int(var)
    elif task_url == 'two_x_close_y':
        answer = round(math.log2(int(var)))
    elif task_url == 'two_x_equal_bin':
        var = int(var, 2)
        answer = round(math.log2(var))
    elif task_url == 'two_x_equal_hex':
        var = int(var, 16)
        answer = round(math.log2(var))
    else:
        answer = round(math.log2(var))
    return answer


def create_twos_complement_arithmetic_task(task, level):
    pass


def get_twos_complement_arithmetic_answer(task_url, task_list):
    pass


def create_big_and_little_endian_byte_order_task(task, level):
    var = randint(2 ** 16 * level, 2 ** 24 * level)
    bytes = math.log2(var) / 8
    bytes_len = bytes + 1 if bytes % 8 == 0 else math.ceil(bytes)
    if task.url == 'x_to_be':
        answer = var.to_bytes(bytes_len, byteorder='big')
    else:
        answer = var.to_bytes(bytes_len, byteorder='little')
    vars_list = [var]
    description = task.description.format(*vars_list)
    return description, str(answer), vars_list


def get_big_and_little_endian_byte_order_answer(task_url, vars_list):
    var = int(vars_list[0])
    bytes = math.log2(var) / 8
    bytes_len = bytes + 1 if bytes % 8 == 0 else math.ceil(bytes)
    if task_url == 'x_to_be':
        answer = var.to_bytes(bytes_len, byteorder='big')
    else:
        answer = var.to_bytes(bytes_len, byteorder='little')
    return answer


def create_pointer_arithmetic_task(task, level):
    pass


def get_pointer_arithmetic_answer(task_url, expression):
    pass


def create_bytes_conversion_task(task, level):
    pass


def get_bytes_conversion_answer(task_url, expression):
    pass


def create_ipv4_subnet_mask_task(task, level):
    pass


def get_ipv4_subnet_mask_answer(task_url, expression):
    pass


def create_ieee_754_floats_task(task, level):
    pass


def get_ieee_754_floats_answer(task_url, expression):
    pass


def create_numeric_limits_task(task, level):
    pass


def get_numeric_limits_answer(task_url, expression):
    pass

