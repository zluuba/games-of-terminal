from inspect import getfullargspec
import functools
import logging
from os import path
from pathlib import Path


BASE_DIR = Path(__file__).parent
LOG_FILENAME = 'got_logs.log'


def get_full_path(base_dir, filename):
    return str(path.join(base_dir, filename))


def get_logger(name='GOT'):
    # LVL:  debug, info, warning, error, critical
    filename = get_full_path(BASE_DIR, LOG_FILENAME)

    # try logging.FileHandler
    logging.basicConfig(
        filename=filename,
        filemode='w',
        format='%(asctime)s : %(levelname)s : %(message)s',
        datefmt='%Y-%m-%d, %H:%M:%S',
        level=logging.DEBUG,
    )
    return logging.getLogger(name)


def get_enter_func_message(func, args, kwargs):
    argspec = getfullargspec(func)
    arg_names = argspec.args

    args_repr = [f"{name}={arg!r}" for name, arg in zip(arg_names, args)]
    kwargs_repr = [f"{key}={val!r}" for key, val in kwargs.items()]
    signature = ", ".join(args_repr + kwargs_repr)

    if signature:
        return (f'Entering function [{func.__name__}] '
                f'with signature: {signature}. '
                f'Module: {func.__module__}.')
    return (f'Entering function [{func.__name__}]. '
            f'Module: {func.__module__}.')


def get_exit_func_message(func, result):
    if result:
        return (f'Function [{func.__name__}] returned result: {result}. '
                f'Module: {func.__module__}.')
    # func.__module__
    return (f'Function [{func.__name__}] returned None. '
            f'Module: {func.__module__}.')


def log(_func=None, *, logger=None, log_type='debug'):
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger_ = logger if logger else get_logger()
            write_log = getattr(logger_, log_type)

            try:
                enter_msg = get_enter_func_message(func, args, kwargs)
                write_log(enter_msg)

                result = func(*args, **kwargs)
                exit_msg = get_exit_func_message(func, result)
                write_log(exit_msg)
                return result

            except Exception as e:
                logger.error(f'Exception raised in {func.__name__}. '
                             f'Exception: {str(e)}.')
                raise e

        return wrapper

    if _func:
        return decorator_log(_func)
    return decorator_log
