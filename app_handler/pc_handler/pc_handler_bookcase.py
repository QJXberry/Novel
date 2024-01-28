# -*-coding:utf-8 -*-
from tornado.web import RequestHandler
from app_base.app_log import error_sen

from app_dao.u_bookcase_dao import count_user_bkcase, find_bk_case_pc, remove_bk_from_case
from settings import BK_NUM_LIMIT
from foundation import get_result, get_int


class PcBookcaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        try:
            u_id = get_int(self.get_cookie("u_id"))
            if not u_id or not u_id:
                self.redirect("/login")
                return
            bk_num = count_user_bkcase(u_id)
            bk_limit = BK_NUM_LIMIT
            bk_list = find_bk_case_pc(u_id)
            self.render("bk_pc/bookcase.html", bk_num=bk_num, bk_limit=bk_limit, bk_list=bk_list)
        except Exception, e:
            error_sen("PcBookcaseHandler", e)

    def post(self, *args, **kwargs):
        u_id = self.get_cookie("u_id")
        if not u_id:
            self.redirect("/login")
            return
        bk_id = self.get_argument("bk_id")
        if bk_id:
            _remove_bk(bk_id, u_id)
            self.write(get_result(code=200, msg="删除成功！"))
            return


def _remove_bk(bk_id, u_id):
    try:
        return remove_bk_from_case(bk_id, u_id)
    except Exception, e:
        error_sen("移除书架书籍", e)