# -*-coding:utf-8 -*-
from tornado.web import RequestHandler
from app_dao.b_book_dao import search_books
from app_service.common_service import get_next_id, get_pre_id
from app_base.app_log import error_sen

from m_handler_class import get_new_bk_list
from settings import PAGE_SIZE, SEARCH_RATE
from app_base.utils import get_remote_ip
from app_base.app_redis import get_cache, set_cache

from foundation import get_int, is_any_blank
from constants.def_redis import SRCH_PRE


class MobileSearchHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self,  *args, **kwargs):
        name = self.get_argument("name").encode('utf-8', "ignore")
        page_index = self.get_argument("page").encode('utf-8', "ignore")
        if is_any_blank(name, page_index):
            return
        result = search_books(name, page_index, PAGE_SIZE)
        total_page = result.get('total_page')
        page_index = result.get('page_index')
        books = result.get('data')
        if books:
            bk_list = get_new_bk_list(books)
            if not bk_list:
                bk_list = []
        else:
            bk_list = []
            page_index = 1
            total_page = 1
        pre_id = get_pre_id(page_index)
        next_id = get_next_id(total_page, page_index)
        self.render('bk_mobile/search.html', bk_list=bk_list, total_page=total_page, page_index=page_index,
                    name=name, pre_id=pre_id, next_id=next_id)


def _set_search_rate(ip, rate):
    try:
        key = SRCH_PRE + ip
        set_cache(key, rate+1, ex=SEARCH_RATE)
    except Exception, e:
        error_sen("_set_search_rate", e)


def _get_search_rate(ip):
    try:
        key = SRCH_PRE + ip
        return get_int(get_cache(key))
    except Exception, e:
        error_sen("_get_search_rate", e)


if __name__ == '__main__':
    pass
    # ip = "127.0.0.1"
    # rate = get_ip_rate(ip)
    # set_ip_rate(ip, rate)
    # print get_ip_rate(ip)