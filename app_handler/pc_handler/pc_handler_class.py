# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from tornado.web import RequestHandler
from app_dao.b_book_dao import select_by_tp_pc, select_wanjie_bk_pc, select_original_bk_pc
from settings import PC_PAGE_SIZE

from constants.def_type_code import get_type_id_m, get_tp_name_pc

from app_base.app_log import error_sen
from app_service.common_service import get_next_id, get_pre_id
from constants.def_type_code import SORT_FINISHED, SORT_ORIGINAL

from app_handler.util_handler import reject_ip
from constants.def_type_code import get_tp_name


class PcClassHandler(RequestHandler):
    def get(self,  *args, **kwargs):
        try:
            # 分类编号
            tp_id = int(args[0])
            # 页数
            page_index = int(args[1])

            if tp_id == SORT_FINISHED:  # 完结
                result = select_wanjie_bk_pc(page_index, PC_PAGE_SIZE)
            elif tp_id == SORT_ORIGINAL:
                result = select_original_bk_pc(page_index, PC_PAGE_SIZE)
            else:
                tp_ids = get_type_id_m(tp_id)
                # 没有这个分类, 封ip
                if tp_ids == 0:
                    reject_ip(self)
                    return
                result = select_by_tp_pc(tp_ids, page_index, PC_PAGE_SIZE)
            total_page = result.get('total_page')
            page_index = result.get('page_index')
            bk_list = result.get('data')
            bk_list = get_new_bk_list(bk_list)
            pre_id = get_pre_id(page_index)
            next_id = get_next_id(total_page, page_index)
            tp_name = get_tp_name_pc(tp_id)
            if not bk_list:
                total_page = 1
                next_id = 1
            self.render('bk_pc/class.html', bk_list=bk_list, total_page=total_page, page_index=page_index,
                        tp_id=tp_id, pre_id=pre_id, next_id=next_id, nav=tp_id, tp_name=tp_name)
        except Exception, e:
            error_sen("PcClassHandler", e, tp_id=tp_id)

    def data_received(self, chunk):
        pass


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
        error_sen("get_new_bk_list", e)