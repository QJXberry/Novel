# -*-coding:utf-8 -*-
from tornado.web import RequestHandler
from app_dao.b_book_dao import search_books_pc

from foundation import is_any_blank
from app_base.app_log import error_sen
from constants.def_type_code import get_tp_name


class PcSearchHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self,  *args, **kwargs):
        name = self.get_argument("name").encode('utf-8', "ignore")
        if is_any_blank(name):
            self.redirect('/')
            return
        bk_list = search_books_pc(name, 10)
        bk_list = get_new_bk_list(bk_list)
        self.render('bk_pc/search.html', bk_list=bk_list)


def get_new_bk_list(books):
    try:
        if not books:
            return ""
        for bk in books:
            tp_id = bk.get('tp_id')
            bk['tp_name'] = get_tp_name(tp_id)
            bk_status = bk.get('bk_status')
            if bk_status == 1:
                bk['bk_status'] = '完结'
            else:
                bk['bk_status'] = '连载'

            bk_lastdate = bk.get("bk_lastdate")
            if bk_lastdate:
                bk["bk_lastdate"] = bk_lastdate.strftime('%Y年%m月%d日')

        return books
    except Exception, e:
        error_sen("get_new_bk_list_2", e)