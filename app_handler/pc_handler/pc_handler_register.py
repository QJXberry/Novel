# -*-coding:utf-8 -*-
from foundation import get_result, is_any_blank
from tornado.web import RequestHandler
from app_base.app_protocol.md5 import re_md5_encrypt

from app_base.utils import get_string, get_remote_ip
from app_dao.u_user_dao import find_id_by_user_name, insert_user
from constants import USER_COMMON

from app_service.util_service import get_now_time

from app_base.app_log import error_sen


class PcRegisterHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self,  *args, **kwargs):
        self.render('bk_pc/register.html')

    def post(self, *args, **kwargs):
        try:
            user_name = get_string(self.get_argument("user_name", strip=True))
            password = get_string(self.get_argument("password", strip=True))
            captcha = get_string(self.get_argument("captcha", strip=True))
            if is_any_blank(user_name, password, captcha):
                self.write(get_result(code=210, msg="参数不全!"))
                return
            # 验证码
            code = self.get_secure_cookie("code")
            if get_string(code) != get_string(captcha):
                self.write(get_result(code=201, msg="验证码错误，请重新输入！"))
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
                self.write(get_result(code=202, msg="该用户已存在， 请重新注册！"))
                return
            else:
                result = insert_user(user_name, password, reg_ip, reg_time, device, USER_COMMON)
                if result:
                    # set_reg_rate(reg_ip, rate)
                    self.write(get_result(code=200, msg="注册成功!"))
                    return
                else:
                    self.write(get_result(code=203, msg="注册失败，请重新注册！"))
                    return

        except Exception, e:
            error_sen("PcRegisterHandler", e)



