from inspect import getfullargspec
from functools import wraps
from logging import basicConfig, getLogger, DEBUG
from os import path
from pathlib import Path
from time import time


BASE_DIR = Path(__file__).parent
LOG_FILENAME = 'got_logs.log'


def get_full_path(base_dir, filename):
    return str(path.join(base_dir, filename))


def get_logger(name='GOT'):
    filename = get_full_path(BASE_DIR, LOG_FILENAME)
    output_format = '%(asctime)s : %(levelname)s : %(message)s'
    date_format = '%Y-%m-%d, %H:%M:%S'

    basicConfig(
        filename=filename,
        filemode='w',
        format=output_format,
        datefmt=date_format,
        level=DEBUG,
    )
    return getLogger(name)


def get_short_module_path(module):
    path_parts = module.split('.')
    return '.'.join(path_parts[1:])


def get_enter_func_message(func, args, kwargs):
    argspec = getfullargspec(func)
    arg_names = argspec.args

    args_repr = [f"{name}={arg!r}" for name, arg in zip(arg_names, args)]
    kwargs_repr = [f"{key}={val!r}" for key, val in kwargs.items()]
    signature = ", ".join(args_repr + kwargs_repr)

    module_short_name = get_short_module_path(func.__module__)

    if signature:
        return (f'Entering function [{func.__name__}] '
                f'with signature: {signature}. '
                f'Module: {module_short_name}.')
    return (f'Entering function [{func.__name__}]. '
            f'Module: {module_short_name}.')


def get_exit_func_message(func, result):
    module_short_name = get_short_module_path(func.__module__)

    if result:
        return (f'Function [{func.__name__}] returned result: {result}. '
                f'Module: {module_short_name}.')
    return (f'Function [{func.__name__}] returned None. '
            f'Module: {module_short_name}.')


def get_func_runtime_message(func, runtime):
    return f'Function [{func.__name__}] runtime is {runtime}ms.'


def get_error_message(func, error):
    return (f'Exception raised in {func.__name__}.'
            f'Exception: {str(error)}.')


def write_logs_with_runtime(func, args, kwargs, write_log_func):
    start_time = time()
    result = func(*args, **kwargs)
    end_time = time()

    runtime_in_sec = end_time - start_time
    runtime_in_ms = round(runtime_in_sec * 1000, 2)
    runtime_message = get_func_runtime_message(func, runtime_in_ms)
    write_log_func(runtime_message)

    return result


def write_logs(write_log_func, func, args, kwargs, with_runtime):
    enter_msg = get_enter_func_message(func, args, kwargs)
    write_log_func(enter_msg)

    if with_runtime:
        result = write_logs_with_runtime(func, args, kwargs, write_log_func)
    else:
        result = func(*args, **kwargs)

    exit_msg = get_exit_func_message(func, result)
    write_log_func(exit_msg)

    return result


def log(_func=None, *, logger=None, log_type='debug', with_runtime=False):
    def decorator_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger_ = logger if logger else get_logger()
            write_log_func = getattr(logger_, log_type)

            try:
                result = write_logs(write_log_func, func,
                                    args, kwargs, with_runtime)
                return result

            except Exception as e:
                error_message = get_error_message(func, e)
                logger_.error(error_message)
                raise e

        return wrapper

    if _func:
        return decorator_log(_func)
    return decorator_log
