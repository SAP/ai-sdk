from __future__ import annotations

import time
import warnings
from functools import lru_cache, wraps
from typing import Dict, Literal, Optional, List, Any, Tuple


def _get_cache_refresh_time(cache_refresh_time: float, recache: bool, timeout: Optional[int] = None) -> float:
    current_time = time.time()
    if recache or (timeout is not None and (current_time - cache_refresh_time) > timeout):
        cache_refresh_time = current_time
    return cache_refresh_time


def _get_cache_key_and_args(cache_refresh_time: float, args: List[Any], first_arg_self: bool) -> Tuple[
    Optional[Any], List[Any], float]:
    if first_arg_self and args:
        id_ = id(args[0])
        cache_key = (id_, cache_refresh_time)
        obj, args = args[0], args[1:]
    else:
        cache_key = (cache_refresh_time,)
        obj = None
    return cache_key, args, obj


def lru_cache_extended(timeout: Optional[int] = None,
                       maxsize: Optional[int] = None,
                       typed: bool = False,
                       first_arg_self: bool = False):
    """Decorator to add LRU caching with optional timeout to methods. 
    Handles 'self' as a weak reference for instance methods if required.

    :param timeout: time in seconds after which the cache will be refreshed. If None, never expires.
    :type timeout: Optional[int], optional
    :param maxsize: maximum size of the cache.
    :type maxsize: Optional[int], optional
    :param typed: if True, arguments of different types will be cached separately.
    :type typed: bool, optional
    :param first_arg_self: if True, treats the first argument as 'self' and uses its id for caching.
    :type first_arg_self: bool, optional
    :return: Decorated method with cache and optional timeout.
    :rtype: Callable
    """

    def decorator(func):
        cache_refresh_time = time.time()

        objs = {}

        @wraps(func)
        @lru_cache(maxsize=maxsize, typed=typed)
        def cached_method(cache_key, *args, **kwargs):
            if first_arg_self:
                id_, _ = cache_key
                args = (objs.pop(id_),) + (args or tuple([]))

            return func(*args, **kwargs)

        @wraps(func)
        def wrapped_func(*args, _recache=False, **kwargs):
            nonlocal cache_refresh_time
            cache_refresh_time = _get_cache_refresh_time(cache_refresh_time, _recache, timeout)
            cache_key, args, obj = _get_cache_key_and_args(cache_refresh_time, args, first_arg_self)
            if obj:
                objs[id(obj)] = obj
            try:
                ret = cached_method(cache_key, *args, **kwargs)
            finally:
                if first_arg_self:
                    objs.pop(id(obj), None)
            return ret

        wrapped_func.cache_info = cached_method.cache_info
        wrapped_func.cache_clear = cached_method.cache_clear

        return wrapped_func

    return decorator


try:
    # Don't duplicate the definition if openai offers it
    from openai._types import NOT_GIVEN, NotGiven
except ImportError:
    class NotGiven:

        def __bool__(self) -> Literal[False]:
            return False

    NOT_GIVEN = NotGiven()


def if_set(value, alternative=NOT_GIVEN):
    """Check if a value is set (not NotGiven and not None), otherwise return an alternative.

    :param value: the value to check.
    :type value: any
    :param alternative: the alternative value to return if the original value is not set.
    :type alternative: any
    :return: The original value if set, otherwise the alternative.
    :rtype: any
    """
    return value if not isinstance(value, NotGiven) and value is not None else alternative

def if_str_set(value: str, alternative: str = ""):
    """Check if a string value is set (not empty), otherwise return an alternative.

    :param value: the string value to check.
    :type value: str
    :param alternative: the alternative string to return if the original value is empty.
    :type alternative: str, optional
    :return: The original string if not empty, otherwise the alternative.
    :rtype: str
    """
    return value if value != "" else alternative

def kwargs_if_set(**kwargs):
    """Filter keyword arguments to include only those that are set (not NotGiven and not None).

    :return: A dictionary of keyword arguments that are set.
    :rtype: Dict[str, any]
    """
    filtered_kwargs = {}
    for name in [*kwargs.keys()]:
        if if_set(kwargs[name]):
            filtered_kwargs[name] = kwargs[name]
    return filtered_kwargs

def warn_once(msg, category=None):
    """Issue a warning only once for a given message.

    :param msg: the warning message.
    :type msg: str
    :param category: the warning category.
    :type category: Optional[Warning], optional
    """
    if not getattr(warn_once, 'log', None):
        warn_once.log = set()
    if msg not in warn_once.log:
        warnings.warn(msg, category, stacklevel=2)
        warn_once.log.add(msg)
