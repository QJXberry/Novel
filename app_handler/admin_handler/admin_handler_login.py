# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_dao.u_user_dao import find_id_type_by_name_pwd
from tornado.web import RequestHandler
from foundation import get_result, is_any_blank, get_string

from app_dao.u_oper_histroy_dao import insert_oper_histroy
from app_base.utils import get_remote_ip
from app_service.util_service import get_now_time

from app_base.app_protocol.md5 import re_md5_encrypt
from app_base.app_log import error_sen
from app_base.app_redis import set_hash_map_cache

from constants.def_redis import U_PRE
import uuid
import time

from constants import USER_ADMIN


class AdminLoginHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self,  *args, **kwargs):
        try:
            # TODO
            self.render('bk_admin/login.html')
        except Exception, e:
            error_sen("AdminLoginHandler get", e)

    def post(self,  *args, **kwargs):
        try:
            user_name = get_string(self.get_argument("user_name"))
            password = get_string(self.get_argument("password"))
            captcha = get_string(self.get_argument("captcha"))
            if is_any_blank(user_name, password, captcha):
                return
            # 验证码
            code = self.get_secure_cookie("code")
            if get_string(code) != get_string(captcha):
                self.write(get_result(ret=1, msg="验证码错误，请重新输入！"))
                return

            password = re_md5_encrypt(password)
            user = find_id_type_by_name_pwd(user_name, password)
            if not user:
                self.write(get_result(ret=2, msg="账号或密码错误！"))
                return
            else:
                u_id = user.get("u_id")
                u_type = user.get("u_type")
                if int(u_type) != USER_ADMIN:
                    self.write(get_result(ret=4, msg="权限不足"))
                    return
                self.set_secure_cookie("user_name", get_string(user_name), expires_days=1)
                self.set_secure_cookie("u_id", str(u_id), expires_days=1)
                self.set_cookie("name", get_string(user_name), expires_days=1)
                token = generate_token(u_id)
                self.set_secure_cookie("token", str(token), expires_days=1)
                ip = get_remote_ip(self)
                oper_time = get_now_time()
                device = self.request.headers.get('User-Agent', '')
                oper_cont = "登录"
                # log
                insert_oper_histroy(u_id, ip, device, oper_cont, oper_time)
                # redis
                result = set_redis_user(u_id, user_name, u_type, token)

                if result:
                    self.write(get_result(ret=0, msg="登录成功！", href='../../static/bk_admin/main.html'))

        except Exception, e:
            error_sen("AdminLoginHandler post", e)


def set_redis_user(u_id, user_name, u_type, token):
    try:
        key = U_PRE + str(u_id)
        return set_hash_map_cache(key, dict(user_name=str(user_name), u_type=str(u_type), token=str(token)), ex=3600 * 24)
    except Exception, e:
        error_sen("set_redis_user_admin", e)


def generate_token(user_id):
    try:
        now = time.time()
        key = get_string(user_id) + get_string(now)
        token = uuid.uuid5(uuid.NAMESPACE_DNS, key)
        return get_string(token)
    except Exception, e:
        error_sen("generate_token", e, user_id=user_id)
