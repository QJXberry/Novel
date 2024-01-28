# -*-coding:utf-8 -*-
from tornado import template

from app_dao.b_book_dao import select_pc_recom, select_pic_bks, select_pc_paihang_index, select_pc_paihang_all
from app_dao.l_link_dao import get_link_list
from app_handler.admin_handler.base_m_handler import BaseHandler
from app_handler.mobile_handler.m_handler_index import get_type_id_m
from app_service.util_service import write_html
from foundation import get_result


class AdminDynamicHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(AdminDynamicHandler, self).__init__(application, request, **kwargs)


def command_create_footer(command):
    """生成底部模块"""
    link_list = get_link_list()
    loader = template.Loader('web/template/bk_pc')
    html = loader.load("T_footer.html").generate(link_list=link_list)
    if write_html(html.decode('utf-8', 'ignore').encode('gbk', "ignore"), "footer", "bk_pc"):
        return get_result(code=200)
    else:
        return get_result(code=201)


def command_create_index_pc(command):
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
    loader = template.Loader('web/template/bk_pc')
    html = loader.load("T_index.html").generate(recom_bks_list=recom_bks_list, xh_pic_bks=xh_pic_bks,
                                                wx_pic_bks=wx_pic_bks, ds_pic_bks=ds_pic_bks,
                                                js_paihang_bks=js_paihang_bks,
                                                all_paihang_bks=all_paihang_bks,
                                                yx_paihang_bks=yx_paihang_bks, kh_paihang_bks=kh_paihang_bks)
    if write_html(html.decode('utf-8', 'ignore').encode('gbk', "ignore"), "index", "bk_pc"):
        return get_result(code=200)
    else:
        return get_result(code=201)


if __name__ == '__main__':
    print command_create_index_pc(1)