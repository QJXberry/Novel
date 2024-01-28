# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from tornado.web import RequestHandler
from app_dao.b_book_dao import find_bk_by_id
from app_dao.b_chapter_dao import find_cp_name_by_bk

from constants.def_type_code import get_tp_name_m
from app_service.util_service import delete_tag


class MobileBkHandler(RequestHandler):
    def get(self,  *args, **kwargs):
        bk_id = args[0]
        book = find_bk_by_id(bk_id)
        if book:
            book["bk_abstract"] = delete_tag(book["bk_abstract"])
            chaps = find_cp_name_by_bk(bk_id)
            bk_status = book.get("bk_status")
            if bk_status == 0:
                book["bk_status"] = "连载中"
            else:
                book["bk_status"] = "已完结"

            book["tp_name"] = get_tp_name_m(book.get("tp_id"))
            bk_lastdate = book.get("bk_lastdate")
            if bk_lastdate:
                book["bk_lastdate"] = bk_lastdate.strftime('%Y年%m月%d日')
            self.render('bk_mobile/book.html', book=book, chaps=chaps)
        else:
            pass

    def data_received(self, chunk):
        pass
