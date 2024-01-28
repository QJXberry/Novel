# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
"""公用方法"""


def get_pre_id(now_id):
    """上一页"""
    if now_id > 1:
        pre_id = now_id - 1
    else:
        pre_id = 1
    return pre_id


def get_next_id(last_id, now_id):
    """下一页"""
    if now_id < last_id:
        next_id = now_id + 1
    else:
        next_id = last_id
    return next_id