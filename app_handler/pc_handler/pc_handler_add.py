# -*-coding:utf-8 -*-
from tornado.web import RequestHandler
from settings import BK_NUM_LIMIT
from foundation import get_result, is_any_blank

from app_dao.u_bookcase_dao import add_book, count_user_bkcase, find_bk
from app_base.app_log import error_sen
from app_dao.b_book_dao import update_bk_read_num


class PcAddHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self,  *args, **kwargs):
        try:
            # 阅读量+1
            bk_id = self.get_argument("bk_id")
            update_bk_read_num(bk_id)

            u_id = self.get_cookie("u_id")
            if not u_id or not int(u_id):
                self.write(get_result(code=1, msg="请先登入!"))
                return

            cp_id = self.get_argument("cp_id")
            cp_name = self.get_argument("cp_name")
            if is_any_blank(bk_id, cp_id, cp_name):
                self.write(get_result(code=2, msg="参数不全!"))
                return
            if not cp_id:
                cp_id = 1

            bk_num = count_user_bkcase(u_id)
            if bk_num >= BK_NUM_LIMIT:
                self.write(get_result(code=4, msg="您的书架已满!"))
                return
            result = add_book(u_id, bk_id, cp_id, cp_name)
            if result:
                self.write(get_result(code=200, msg="加入成功!"))
                return
            else:
                self.write(get_result(code=3, msg="加入失败!"))
                return
        except Exception, e:
            error_sen("PcAddHandler", e)

