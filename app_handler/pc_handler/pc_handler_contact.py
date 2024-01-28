# -*-coding:utf-8 -*-
from tornado.web import RequestHandler
from foundation import is_any_blank, get_result
from app_service.util_service import delete_tag

from app_dao.m_message_dao import inset_msg
from app_base.utils import get_remote_ip
from urllib import unquote


class PcContactHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self,  *args, **kwargs):
        self.render("bk_pc/contact.html")

    def post(self, *args, **kwargs):
        try:
            msg_name = self.get_argument("msg_name")
            msg_phone = self.get_argument("msg_phone")
            msg_cont = self.get_argument("msg_cont")
            if is_any_blank(msg_name, msg_phone, msg_cont):
                self.write(get_result(ret=2, msg="参数不全!"))
                return
            msg_name = delete_tag(msg_name)
            msg_phone = delete_tag(msg_phone)
            msg_cont = delete_tag(msg_cont)
            u_id = self.get_cookie("u_id")
            user_name = self.get_cookie("user_name") or ""
            user_name = unquote(user_name)
            msg_ip = delete_tag(get_remote_ip(self))
            reslut = inset_msg(u_id, user_name, msg_name, msg_phone, msg_cont, msg_ip)
            if reslut:
                self.write(get_result(ret=0, msg="留言成功!"))
                return
            else:
                self.write(get_result(ret=1, msg="留言失败!"))
                return
        except Exception, e:
            print "pc_handler_Contact ERROR:", str(e)
