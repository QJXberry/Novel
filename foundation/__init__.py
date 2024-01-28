# coding:utf8
from app_base.app_db import db_query_for_int, db_query_for_dict, get_int
from sys import maxint
from app_base.app_redis import get_hash_map_cache
from app_base.utils import get_int, get_string
'''
    常用/公共函数包
'''


def get_result(**kwargs):
    """
    """
    result = {}
    for k, v in kwargs.iteritems():
        result[k] = v
    return result


def is_any_blank(*args):
    """*args存在空就返回1, 全部非空返回0"""
    for a in args:
        if is_not_blank(a) == 0:
            return 1
    return 0


def is_not_blank(s):
    """空返回0, 非空返回1"""
    if s is None:
        return 0
    s = str(s)
    return s.strip() and 1 or 0


if __name__ == '__main__':
    print get_result(a="b", d="d")