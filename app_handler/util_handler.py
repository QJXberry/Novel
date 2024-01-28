# -*-coding:utf-8 -*-
from foundation import is_any_blank, get_int, get_string
from app_base.app_redis import get_cache, set_cache
from constants.def_redis import U_PRE, IP_PRE

from app_base.utils import get_remote_ip
from app_base.app_log import error_sen


def ip_rate_limit(func):
    """访问频率限制"""
    def _wrapper(self, *args, **kwargs):
        ip = get_remote_ip(self)
        rate = _get_ip_rate(ip)
        if rate > 20:
            reject_ip(self)
            return
        else:
            # 增频
            # _set_ip_rate(ip, rate, ex=2)
            return func(self, *args, **kwargs)
    return _wrapper


def _set_ip_rate(ip, rate, ex):
    try:
        key = IP_PRE + ip
        set_cache(key, rate+1, ex=ex)
    except Exception, e:
        error_sen("_set_ip_rate", e)


def _get_ip_rate(ip):
    try:
        key = IP_PRE + ip
        return get_int(get_cache(key))
    except Exception, e:
        error_sen("_get_ip_rate", e)


def reject_ip(self, rej_time=60*60*6):
    """rej_time (s)"""
    try:
        ip = get_remote_ip(self)
        self.write("非法操作，拒绝访问！请联系管理员~")
        _set_ip_rate(ip, 555, ex=rej_time)
    except Exception, e:
        error_sen("reject_ip", e)


def get_referer(self):
    try:
        referer = self.request.headers['referer']
        return referer
    except:
        return "/"
