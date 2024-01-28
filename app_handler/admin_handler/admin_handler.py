# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_log import error_sen
from app_base.app_protocol.md5 import re_md5_encrypt
from app_base.utils import get_string
from app_dao.b_book_dao import get_count_bks, get_recom_list, change_recom_bk, set_recom_bk, get_recom_top_list,\
    update_sort

from app_dao.b_chapter_dao import get_count_cps
from app_dao.l_link_dao import get_link_list, del_link, insert_link
from app_dao.m_message_dao import get_count_msg, inset_reply_msg, get_msg_paging
from app_dao.m_ad_dao import *

from app_dao.u_user_dao import get_count_users, insert_user, del_user, get_user_list_paging, find_id_by_user_name
from app_handler.admin_handler.base_m_handler import BaseHandler
from app_service.util_service import write_txt
from app_service.util_service import get_now_time

from foundation import get_result
from foundation import is_any_blank
from foundation.del_tag import parsehtml
from app_dao.b_chapter_dao import update_chap

from app_handler.admin_handler import check_login, clean
from app_service.admin_service.service_book import del_bk, del_cp
from settings import AD_PATH, PIC_PATH
from app_dao.a_announce_dao import get_announce_list, del_announce, insert_announce
import time

import StringIO
from app_dao.b_book_dao import find_bk_by_name, add_new_bk, get_last_cp_id, update_author_bk
from app_dao.b_chapter_dao import add_chap
from app_service.util_service import num_to_chinese


class AdminHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(AdminHandler, self).__init__(application, request, **kwargs)


@check_login
def command_total_books(command):
    """总书数"""
    return get_count_bks()


@check_login
def command_total_chapters(command):
    """总章节数"""
    return get_count_cps()


@check_login
def command_total_users(command):
    """总用户数"""
    return get_count_users()


@check_login
def command_total_message(command):
    """总留言数"""
    return get_count_msg()


# @check_login
# def command_change_pic(command):
#     """更换封面"""
#     bk_name = command.params.get('bk_name')
#     pic_num = int(command.params.get('pic_num'))
#     if is_any_blank(bk_name):
#         return get_result(code=201, msg="参数不全")
#
#     result = change_pic(bk_name, pic_num)
#     if result:
#         return get_result(code=200)
#     else:
#         return get_result(code=201)


@check_login
def command_recom_list(command):
    """小鸡推荐列表"""
    try:
        return get_result(code=200, data=eval(clean(get_recom_list())))
    except Exception, e:
        error_sen("command_recom_list", e)
        return get_result(code=201)


@check_login
def command_del_recom(command):
    """删除推荐"""
    try:
        bk_id = command.params.get('bk_id')
        result = change_recom_bk(bk_id, 0)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_change_recom", e)
        return get_result(code=201)


@check_login
def command_set_recom(command):
    """设置推荐"""
    try:
        bk_name = command.params.get('bk_name')

        if is_any_blank(bk_name):
            return get_result(code=201, msg="参数不全")

        result = set_recom_bk(bk_name)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_set_recom", e)
        return get_result(code=201)


@check_login
def command_sort_list(command):
    """查看优先级最高的前50本"""
    try:
        result = get_recom_top_list()
        return get_result(code=200, data=result)
    except Exception, e:
        error_sen("command_recom_list", e)


@check_login
def command_update_sort(command):
    """修改优先级"""
    try:
        bk_name = command.params.get('bk_name')
        bk_sort = command.params.get('bk_sort')

        if is_any_blank(bk_name, bk_sort):
            return get_result(code=201, msg="参数不全")

        result = update_sort(bk_sort, bk_name)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_update_sort", e)


@check_login
def command_link_list(command):
    """友情链接"""
    try:
        result = get_link_list()
        if result:
            result = eval(clean(result))
            return get_result(code=200, data=result)
    except Exception, e:
        error_sen("command_link_list", e)


@check_login
def command_del_link(command):
    """删除友情链接"""
    try:
        id = command.params.get('id')
        result = del_link(id)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_del_link", e)


@check_login
def command_set_link(command):
    """添加友情链接"""
    try:
        link_name = command.params.get('link_name')
        link_address = command.params.get('link_address')
        link_sort = command.params.get('link_sort')
        if is_any_blank(link_name, link_address, link_sort):
            return get_result(code=201, msg="参数不全")

        result = insert_link(link_name, link_address, link_sort)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_set_link", e)


@check_login
def command_reply_msg(command):
    """回复留言"""
    try:
        u_id = command.params.get('u_id')
        msg_cont = command.params.get('msg_cont')
        if is_any_blank(u_id, msg_cont):
            return get_result(code=201, msg="参数不全")
        result = inset_reply_msg(u_id, msg_cont, command.ip)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_reply_msg", e)


@check_login
def command_message(command):
    """查看留言"""
    try:
        page_index = command.params.get('page_index')
        result = get_msg_paging(int(page_index))
        if result:
            result = eval(clean(result))
            return get_result(code=200, data=result)
    except Exception, e:
        error_sen("command_message", e)


@check_login
def command_add_user(command):
    """添加用户"""
    try:
        user_name = command.params.get('user_name')
        password = command.params.get('password')
        u_type = command.params.get('u_type')
        if is_any_blank(user_name, password, u_type):
            return get_result(code=201, msg="参数不全")

        u_id = find_id_by_user_name(user_name)
        if u_id:
            return get_result(code=201, msg="该用户已存在")

        password = re_md5_encrypt(get_string(password))
        reg_ip = command.ip
        reg_time = get_now_time()
        device = command.device
        result = insert_user(user_name, password, reg_ip, reg_time, device, u_type)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_message", e)


@check_login
def command_del_user(command):
    """删除用户"""
    try:
        u_id = command.params.get('u_id')

        if is_any_blank(u_id):
            return get_result(code=201, msg="参数不全")

        result = del_user(u_id)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_del_user", e)


@check_login
def command_user_list(command):
    """用户列表"""
    try:
        page_index = command.params.get('page_index')
        result = get_user_list_paging(page_index)
        if result:
            result = eval(clean(result))
            return get_result(code=200, data=result)
    except Exception, e:
        error_sen("command_user_list", e)


@check_login
def command_del_bk(command):
    """删除整本书的txt"""
    try:
        bk_id = command.params.get("bk_id")
        if is_any_blank(bk_id):
            return get_result(code=201, msg="参数不全")

        result = del_bk(bk_id)
        if result is True:
            return get_result(code=200)
        else:
            return get_result(code=201, msg=result)
    except Exception, e:
        error_sen("command_del_tests", e)
        

@check_login
def command_del_cp(command):
    """删除章节"""
    try:
        bk_id = command.params.get("bk_id")
        cp_id = command.params.get("cp_id")
        if is_any_blank(bk_id, cp_id):
            return get_result(code=201, msg="参数不全")
        if del_cp(bk_id, cp_id):
            return get_result(code=200)
    except Exception, e:
        error_sen("command_del_cp", e)


@check_login
def command_add_ad(command):
    """添加广告"""
    try:
        files = command.files
        ad_description = command.params.get("ad_description")
        ad_url = command.params.get("ad_url")
        img = files[0]
        if is_any_blank(ad_description, ad_url, img):
            return get_result(code=201, msg="参数不全,请填写完整")
        file_name = str(int(time.time() * 1000))
        ad_path = AD_PATH + '/' + file_name + '.jpg'
        with open(ad_path, 'wb') as f:
            f.write(img['body'])

        result = insert_ad(ad_description, ad_url, file_name)
        if result:
            return get_result(code=200)
        else:
            return get_result(code=201)
    except Exception, e:
        error_sen("command_add_ad", e)


@check_login
def command_get_ad(command):
    """广告列表"""
    try:
        result = get_ad_list()
        if result:
            result = eval(clean(result))
            return get_result(code=200, data=result)
    except Exception, e:
        error_sen("command_get_ad", e)


@check_login
def command_get_announce(command):
    """公告列表"""
    try:
        result = get_announce_list()
        if result:
            result = eval(clean(result))
            return get_result(code=200, data=result)
    except Exception, e:
        error_sen("command_get_announce", e)


@check_login
def command_del_announce(command):
    """删除公告"""
    try:
        a_id = command.params.get("a_id")
        if is_any_blank(a_id):
            return get_result(code=201, msg="参数不全")

        result = del_announce(a_id)
        if result:
            return get_result(code=200)
        else:
            return get_result(code=201, msg=result)
    except Exception, e:
        error_sen("command_del_ad", e)


@check_login
def command_add_announce(command):
    """添加公告"""
    try:
        a_announce = command.params.get('a_announce')
        sort = command.params.get('sort')
        red = command.params.get('red')
        if is_any_blank(a_announce, sort, red):
            return get_result(code=201, msg="参数不全")

        result = insert_announce(a_announce, sort, red)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_set_link", e)


@check_login
def command_del_ad(command):
    """删除广告"""
    try:
        ad_id = command.params.get("id")
        if is_any_blank(ad_id):
            return get_result(code=201, msg="参数不全")

        result = del_ad(ad_id)
        if result:
            return get_result(code=200)
        else:
            return get_result(code=201, msg=result)
    except Exception, e:
        error_sen("command_del_ad", e)


@check_login
def command_change_pic(command):
    """更换新的封面"""
    try:
        bk_id = command.params.get("bk_id")
        files = command.files
        img = files[0]
        if is_any_blank(bk_id, img):
            return get_result(code=201, msg="参数不全,请填写完整")
        file_name = str(bk_id)
        pic_path = PIC_PATH + '/' + file_name + '.jpg'
        with open(pic_path, 'wb') as f:
            f.write(img['body'])
        return get_result(code=200)
    except Exception, e:
        error_sen("command_change_pic", e)


@check_login
def command_upload_txt(command):
    """上传整书"""
    try:
        bk_name = command.params.get("bk_name")
        bk_author = command.params.get("bk_author")
        tp_id = command.params.get("tp_id")
        bk_abstract = command.params.get('bk_abstract')
        files = command.files
        txt = files[0]
        if is_any_blank(bk_name, bk_author, txt, tp_id, bk_abstract):
            return get_result(code=201, msg="参数不全,请填写完整")

        all_txt = StringIO.StringIO(txt.get('body').decode('gbk'))
        txt = all_txt.read().strip()
        line = all_txt.readlines()
        txt = txt.replace('\n', '<br/>')

        all_txt.close()
        chaps_num = len(txt) / 3000 + 1 if len(txt) % 3000 else len(txt) / 3000
        # 保存书籍信息
        if find_bk_by_name(bk_name):
            return get_result(code=202, msg="该书名已存在")
        bk_id = add_new_bk(bk_name, bk_author, tp_id, bk_abstract)
        print bk_id
        cp_id = get_last_cp_id(bk_id)
        for i in range(1, chaps_num+1):
            cp_id += 1
            cp_content = txt[(i-1)*3000: i*3000]
            # 保存章节
            cp_words = len(cp_content)
            # 写入本地文件

            result_write = write_txt(get_string(cp_content), bk_id, cp_id)
            print result_write
            if not result_write:
                return
            # 插入章节表
            cp_name = "第%s章" % num_to_chinese(i).encode("utf-8")
            result_chap = add_chap(bk_id, cp_name, cp_id, cp_words)
            if not result_chap:
                return
        # 更新bk表
        result = update_author_bk(bk_id, cp_name, cp_id)
        return get_result(code=200)
    except Exception, e:
        error_sen("command_upload_txt", e)


@check_login
def command_update_chap(command):
    """修改章节"""
    try:
        bk_id = command.params.get('bk_id')
        cp_id = command.params.get('cp_id')
        cp_name = command.params.get('cp_name')
        cp_content = command.params.get('cp_content')
        cp_content = parsehtml(cp_content)
        print command.params
        if is_any_blank(bk_id, cp_name, cp_content, cp_id):
            return

        cp_words = len(cp_content) / 3

        # 写入本地文件
        result_write = write_txt(cp_content, bk_id, cp_id)
        if not result_write:
            return
        result = update_chap(bk_id, cp_name, cp_id, cp_words)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_update_chap", e)


if __name__ == '__main__':
    print num_to_chinese(4)
    print type(num_to_chinese(1))