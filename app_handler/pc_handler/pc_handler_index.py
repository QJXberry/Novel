# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from tornado.web import RequestHandler
from app_dao.l_link_dao import get_link_list
from app_dao.b_book_dao import select_pc_recom, select_pic_bks, select_pc_paihang_index, select_pc_paihang_all

from app_handler.mobile_handler.m_handler_index import get_type_id_m
from foundation import get_result


class PcIndexHandler(RequestHandler):
    # def get(self,  *args, **kwargs):
    #     self.render('bk_pc/index.html')

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        """生成首页"""
        xh = get_type_id_m(1)
        wx = get_type_id_m(2)
        ds = get_type_id_m(3)
        js = get_type_id_m(4)
        yx = get_type_id_m(5)
        kh = get_type_id_m(6)
        """首页小鸡推荐"""
        recom_bks_list = select_pc_recom()

        """首页有封面的"""
        xh_pic_bks = select_pic_bks(xh, 6)
        wx_pic_bks = select_pic_bks(wx, 6)
        ds_pic_bks = select_pic_bks(ds, 6)
        """首页排行的"""
        js_paihang_bks = select_pc_paihang_index(js, 10)
        yx_paihang_bks = select_pc_paihang_index(yx, 10)
        kh_paihang_bks = select_pc_paihang_index(kh, 10)
        all_paihang_bks = select_pc_paihang_all(10)
        """友情链接"""
        self.render('bk_pc/T_index.html', recom_bks_list=recom_bks_list, xh_pic_bks=xh_pic_bks,
                                                    wx_pic_bks=wx_pic_bks, ds_pic_bks=ds_pic_bks,
                                                    js_paihang_bks=js_paihang_bks,
                                                    all_paihang_bks=all_paihang_bks,
                                                    yx_paihang_bks=yx_paihang_bks, kh_paihang_bks=kh_paihang_bks)

    def post(self, *args, **kwargs):
        link_list = get_link_list()
        self.write(get_result(data=link_list))