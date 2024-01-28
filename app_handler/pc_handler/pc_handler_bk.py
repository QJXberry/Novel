# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from tornado.web import RequestHandler
from app_dao.b_book_dao import find_bk_by_id
from app_dao.b_chapter_dao import find_cp_name_by_bk

from constants.def_type_code import get_tp_name_m, get_class_id


class PcBkHandler(RequestHandler):
    def get(self,  *args, **kwargs):
        bk_id = args[0]
        book = find_bk_by_id(bk_id)
        if book:
            chaps = find_cp_name_by_bk(bk_id)
            book["tp_name"] = get_tp_name_m(book.get("tp_id"))
            tp_id = get_class_id(book.get("tp_id"))
            self.render('bk_pc/novel.html', book=book, chaps=chaps, tp_id=tp_id)
        else:
            self.redirect("/error")

    def data_received(self, chunk):
        pass
