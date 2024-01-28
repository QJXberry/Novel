# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from foundation import is_any_blank, get_string
from constants.def_redis import U_PRE
from app_base.app_redis import get_hash_cache

from constants import USER_ADMIN
from app_base.utils import sequence_to_string
from cgi import escape


def check_login(func):
    """检验登入"""
    def _wrapper(command_info):
        u_id = command_info.u_id
        user_name = command_info.user_name
        token = command_info.token
        if is_any_blank(u_id, user_name, token):
            return
        else:
            # 校验 id 和 用户名是否匹配
            _user_name = get_string(_get_redis_user(u_id, "user_name"))
            _token = get_string(_get_redis_user(u_id, "token"))
            if _user_name != user_name or _token != token:
                # 伪造的用户cookie,
                return
            else:
                _u_type = int(_get_redis_user(u_id, "u_type"))
                if _u_type == USER_ADMIN:
                    return func(command_info)
    return _wrapper


def _get_redis_user(u_id, key):
    name = U_PRE + u_id
    return get_hash_cache(name, key)


def clean(data):
    """xss过滤"""
    try:
        s = str(sequence_to_string(data))
        s = escape(s)
        return s
    except Exception, e:
        print "clean", e