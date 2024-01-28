# -*-coding:utf-8 -*-
from tornado.web import RequestHandler
from app_dao.b_book_dao import select_by_tp, select_wanjie_bk, select_paihang_bks, select_original_bks
from settings import PAGE_SIZE

from constants import DAY_ONE
from constants.def_type_code import get_type_id_m, get_tp_name
import datetime

from app_base.app_log import error_sen
from app_service.common_service import get_next_id, get_pre_id
from constants.def_type_code import SORT_ALL, SORT_FINISHED, SORT_ORIGINAL

from app_handler.util_handler import ip_rate_limit, reject_ip
from constants.def_type_code import get_tp_name_pc
from app_dao.b_book_dao import select_index_bks_by_tp


class MobileClassHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        try:
            # 分类编号
            tp_id = int(args[0])
            # 页数
            page_index = int(args[1])

            if tp_id == SORT_FINISHED:  # 完结
                result = select_wanjie_bk(page_index, PAGE_SIZE)
            elif tp_id == SORT_ALL:  # 总排行
                get_paihang(self)
                return
            elif tp_id == SORT_ORIGINAL:  # 原创
                result = select_original_bks(page_index, PAGE_SIZE)
            else:
                tp_ids = get_type_id_m(tp_id)
                # 没有这个分类, 封ip
                if tp_ids == 0:
                    reject_ip(self)
                    return
                result = select_by_tp(tp_ids, page_index, PAGE_SIZE)
            total_page = result.get('total_page')
            page_index = result.get('page_index')
            books = result.get('data')
            bk_list = get_new_bk_list(books)
            pre_id = get_pre_id(page_index)
            next_id = get_next_id(total_page, page_index)
            if not bk_list:
                total_page = 1
                next_id = 1
            tp_name = get_tp_name_pc(tp_id)
            self.render('bk_mobile/class.html', bk_list=bk_list, total_page=total_page, page_index=page_index,
                        tp_id=tp_id, pre_id=pre_id, next_id=next_id, tp_name=tp_name)
            return
        except Exception, e:
            error_sen("MobileClassHandler", e)


def get_paihang(self):
    rmxs = select_index_bks_by_tp(get_type_id_m(1), 7)
    rzxy = select_index_bks_by_tp(get_type_id_m(2), 7)
    rzgy = select_index_bks_by_tp(get_type_id_m(3), 7)
    rzhy = select_index_bks_by_tp(get_type_id_m(4), 7)
    rmnp = select_index_bks_by_tp(get_type_id_m(5), 7)
    rmxs_list = get_new_bk_list(rmxs)
    rzxy_list = get_new_bk_list(rzxy)
    rzgy_list = get_new_bk_list(rzgy)
    rzhy_list = get_new_bk_list(rzhy)
    rmnp_list = get_new_bk_list(rmnp)
    self.render('bk_mobile/paihang.html', rmxs_list=rmxs_list, rzxy_list=rzxy_list,
                rzgy_list=rzgy_list, rzhy_list=rzhy_list, rmnp_list=rmnp_list)
    return


def get_new_bk_list(books):
    try:
        if not books:
            return ""
        this_day = datetime.datetime.now()
        bk_list = []
        for bk in books:
            bk_id = bk.get("bk_id")
            tp_id = bk.get("tp_id")
            bk_lastdate = bk.get("bk_lastdate") or this_day
            bk_author = bk.get("bk_author")
            bk_status = bk.get("bk_status")
            bk_name = bk.get("bk_name")
            bk_abstract = bk.get("bk_abstract")
            if bk_status == 1:
                bk_ball = "three"
            else:
                diff_day = (this_day - bk_lastdate).days
                if diff_day <= DAY_ONE:
                    bk_ball = "one"
                else:
                    bk_ball = "two"
            tp_name = get_tp_name(tp_id)
            bk_list.append(dict(
                bk_id=bk_id,
                bk_name=bk_name,
                bk_author=bk_author,
                tp_name=tp_name,
                bk_ball=bk_ball,
                bk_abstract=bk_abstract
            ))
        return bk_list
    except Exception, e:
        error_sen("get_new_bk_list", e)
