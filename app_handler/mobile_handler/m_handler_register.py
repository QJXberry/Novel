# -*-coding:utf-8 -*-
from foundation import get_result, is_any_blank
from tornado.web import RequestHandler
from app_base.app_protocol.md5 import re_md5_encrypt

from app_base.utils import get_int, get_string, get_remote_ip
from app_dao.u_user_dao import find_id_by_user_name, insert_user
from constants import USER_WRITER, USER_COMMON

from app_service.util_service import get_now_time
from app_base.app_redis import get_cache, set_cache
from constants.def_redis import REG_PRE

from app_base.app_log import error_sen
from settings import REG_RATE
from app_handler.util_handler import get_referer


class MobileRegisterHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self,  *args, **kwargs):
        referer = get_referer(self)
        self.render('bk_mobile/register.html', referer=referer)

    def post(self, *args, **kwargs):
        try:
            user_name = get_string(self.get_argument("user_name", strip=True))
            password = get_string(self.get_argument("password", strip=True))
            captcha = get_string(self.get_argument("captcha", strip=True))
            if is_any_blank(user_name, password, captcha):
                self.write(get_result(ret=10, msg="参数不全!"))
                return
            # 验证码
            code = self.get_secure_cookie("code")
            if get_string(code) != get_string(captcha):
                self.write(get_result(ret=1, msg="验证码错误，请重新输入！"))
                return

            device = self.request.headers.get('User-Agent', '')
            reg_time = get_now_time()
            # MD5
            password = re_md5_encrypt(get_string(password))
            reg_ip = get_remote_ip(self)
            # 限制频率, 注册后1小时内不能在再次注册
            # rate = get_reg_rate(reg_ip)
            # if rate:
            #     self.write(get_result(ret=4, msg="注册过于频繁!"))
            #     return
            # 查看用户名是否被注册过
            u_id = find_id_by_user_name(user_name)
            if u_id:
                self.write(get_result(ret=2, msg="该用户已存在， 请重新注册！"))
                return
            else:
                result = insert_user(user_name, password, reg_ip, reg_time, device, USER_COMMON)
                if result:
                    # set_reg_rate(reg_ip, rate)
                    self.write(get_result(ret=0, msg="注册成功!"))
                    return
                else:
                    self.write(get_result(ret=3, msg="注册失败，请重新注册！"))
                    return

        except Exception, e:
            error_sen("MobileRegisterHandler", e)


def set_reg_rate(ip, rate):
    try:
        key = REG_PRE + ip
        set_cache(key, rate+1, ex=REG_RATE)
    except Exception, e:
        error_sen("set_reg_rate", e)


def get_reg_rate(ip):
    try:
        key = REG_PRE + ip
        return get_int(get_cache(key))
    except Exception, e:
        error_sen("get_reg_rate", e)

if __name__ == '__main__':
    print get_reg_rate("127.0.0.1")