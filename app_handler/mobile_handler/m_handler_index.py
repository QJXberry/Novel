# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from tornado.web import RequestHandler
from app_dao.b_book_dao import select_recom_bks
import datetime

from constants import DAY_ONE
from app_base.app_log import error_sen
from app_dao.b_book_dao import select_index_bks_by_tp, select_index_bks_by_time
from app_dao.a_announce_dao import get_announce_list

from constants.def_type_code import get_type_id_m
from m_handler_class import get_new_bk_list
from app_service.util_service import delete_tag
from app_dao.m_ad_dao import get_ad_list


class MobileIndexHandler(RequestHandler):

    def get(self,  *args, **kwargs):
        recom_bks = select_recom_bks(3)
        recom_bks_list = get_rec_bk_list(recom_bks)
        rmxs = select_index_bks_by_tp(get_type_id_m(1))
        rzxy = select_index_bks_by_tp(get_type_id_m(2))
        rzgy = select_index_bks_by_tp(get_type_id_m(3))
        rzhy = select_index_bks_by_tp(get_type_id_m(4))
        rmnp = select_index_bks_by_tp(get_type_id_m(5))
        rdca = select_index_bks_by_tp(get_type_id_m(6))
        jctr = select_index_bks_by_time()  # 排行

        rmxs_list = get_new_bk_list(rmxs)
        rzxy_list = get_new_bk_list(rzxy)
        rzgy_list = get_new_bk_list(rzgy)
        rzhy_list = get_new_bk_list(rzhy)
        rmnp_list = get_new_bk_list(rmnp)
        rdca_list = get_new_bk_list(rdca)
        jctr_list = get_new_bk_list(jctr)

        new_list = get_ad_list()
        announce = get_announce_list()
        self.render('bk_mobile/index.html', recom_bks=recom_bks_list, rmxs_list=rmxs_list, rzxy_list=rzxy_list,
                    rzgy_list=rzgy_list, rzhy_list=rzhy_list, rmnp_list=rmnp_list, rdca_list=rdca_list,
                    jctr_list=jctr_list, new_list=new_list, announce=announce)

    def data_received(self, chunk):
        pass


def get_rec_bk_list(books):
    try:
        this_day = datetime.datetime.now()
        bk_list = []
        for bk in books:
            bk_id = bk.get("bk_id")
            bk_lastdate = bk.get("bk_lastdate") or this_day
            bk_author = bk.get("bk_author")
            bk_status = bk.get("bk_status")
            bk_name = bk.get("bk_name")
            bk_abstract = bk.get("bk_abstract")
            bk_abstract = delete_tag(bk_abstract)
            if bk_status == 1:
                bk_ball = "three"
            else:
                diff_day = (this_day - bk_lastdate).days
                if diff_day <= DAY_ONE:
                    bk_ball = "one"
                else:
                    bk_ball = "two"
            bk_list.append(dict(
                bk_id=bk_id,
                bk_name=bk_name,
                bk_author=bk_author,
                bk_ball=bk_ball,
                bk_abstract=bk_abstract
            ))
        return bk_list
    except Exception, e:
        error_sen("get_new_bk_list", e)