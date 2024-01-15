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
        datefmt='%H:%M:%S',
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
        return (f'Entering function {func.__name__} '
                f'from {func.__module__} with signature: {signature}.')
    return f'Entering function {func.__name__} from {func.__module__}.'


def get_exit_func_message(func, result):
    if result:
        return (f'Function {func.__name__} '
                f'from {func.__module__} returned result: {result}.')
    # func.__module__
    return (f'Function {func.__name__} '
            f'from {func.__module__} returned None.')


def log(func, base_logger=None, log_level='debug'):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger() if base_logger is None else base_logger
        write_log = getattr(logger, log_level)

        try:
            enter_msg = get_enter_func_message(func, args, kwargs)
            write_log(enter_msg)

            result = func(*args, **kwargs)
            exit_msg = get_exit_func_message(func, result)
            write_log(exit_msg)
            return result

        except Exception as e:
            logger.error(f'Exception raised in {func.__name__}. '
                         f'Function dict: {func.__dict__}.'
                         f'Exception: {str(e)}.')
            raise e

    return wrapper
