# -*-coding:utf-8 -*-
from app_dao.u_user_dao import find_id_by_name_pwd
from tornado.web import RequestHandler
from foundation import get_result, is_any_blank, get_string

from app_dao.u_oper_histroy_dao import insert_oper_histroy
from app_base.utils import get_remote_ip
from app_service.util_service import get_now_time

from app_base.app_redis import set_cache
from constants.def_redis import U_PRE
from app_base.app_protocol.md5 import re_md5_encrypt

from app_handler.util_handler import get_referer
from urllib import quote


class MobileLoginHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self,  *args, **kwargs):
        referer = get_referer(self)
        self.render('bk_mobile/login.html', referer=referer)

    def post(self, *args, **kwargs):
        try:
            user_name = get_string(self.get_argument("user_name", strip=True))
            password = get_string(self.get_argument("password", strip=True))
            if is_any_blank(user_name, password):
                self.write(get_result(code=201, msg="参数不全！"))
                return
            password = re_md5_encrypt(password)
            u_id = find_id_by_name_pwd(user_name, password)
            if not u_id:
                self.write(get_result(code=202, msg="账号或密码错误！"))
                return
            else:
                self.set_cookie("user_name", quote(user_name), expires_days=900)
                self.set_cookie("u_id", str(u_id), expires_days=900)
                self.set_cookie("status", str(1), expires_days=900)
                ip = get_remote_ip(self)
                oper_time = get_now_time()
                device = self.request.headers.get('User-Agent', '')
                oper_cont = "登录手机端"
                # log
                insert_oper_histroy(u_id, ip, device, oper_cont, oper_time)
                self.write(get_result(code=200, msg="登录成功！"))
                return
        except Exception, e:
            print "m_handler_Login ERROR:", str(e)



