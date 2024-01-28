# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_log import error_sen
from app_handler.admin_handler.base_m_handler import BaseHandler
from app_dao.b_book_dao import add_new_bk, get_my_bk, get_last_cp_id, update_author_bk, find_bk_by_name, \
    select_author_by_id, select_author_by_name, update_bk_status

from foundation import get_result, is_any_blank
from foundation.del_tag import parsehtml
from app_dao.b_chapter_dao import add_chap, update_chap, get_my_cp, search_my_cp
from app_service.util_service import num_to_chinese

from app_service.util_service import write_txt, list_to_str
from app_handler.writer_handler import check_login
import StringIO
from app_base.utils import get_string


class WriterHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super(WriterHandler, self).__init__(application, request, **kwargs)


@check_login
def command_add_bk(command):
    """添加新书"""
    try:
        bk_name = command.params.get('bk_name')
        bk_author = command.user_name
        tp_id = command.params.get('tp_id')
        bk_abstract = command.params.get('bk_abstract')
        bk_abstract = parsehtml(bk_abstract)
        if is_any_blank(bk_author, bk_name, tp_id, bk_abstract):
            return
        if find_bk_by_name(bk_name):
            return get_result(code=202, msg="该书名已存在")
        result = add_new_bk(bk_name, bk_author, tp_id, bk_abstract)
        if result:
            return get_result(code=200)
        else:
            return get_result(code=201)
    except Exception, e:
        error_sen("command_add_bk", e)


@check_login
def command_my_bk(command):
    """获取作者的书列表"""
    try:
        bk_author = command.user_name
        if not bk_author:
            return
        result = get_my_bk(bk_author)
        if result:
            return get_result(code=200, data=result)
    except Exception, e:
        error_sen("command_my_bk", e)


@check_login
def command_add_chap(command):
    """新增章节"""
    try:
        bk_id = command.params.get('bk_id')
        cp_name = command.params.get('cp_name')
        cp_content = command.params.get('cp_content')
        cp_content = parsehtml(cp_content)
        if is_any_blank(bk_id, cp_name, cp_content):
            return

        cp_words = len(cp_content) / 3
        cp_id = get_last_cp_id(bk_id) + 1
        # 写入本地文件
        result_write = write_txt(cp_content, bk_id, cp_id)
        if not result_write:
            return
        # 插入章节表
        result_chap = add_chap(bk_id, cp_name, cp_id, cp_words)
        if not result_chap:
            return
        # 更新bk表
        result = update_author_bk(bk_id, cp_name, cp_id)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_add_chap", e)


@check_login
def command_update_chap(command):
    """修改章节"""
    try:
        bk_id = command.params.get('bk_id')
        cp_id = command.params.get('cp_id')
        cp_name = command.params.get('cp_name')
        cp_content = command.params.get('cp_content')
        cp_content = parsehtml(cp_content)

        if is_any_blank(bk_id, cp_name, cp_content, cp_id):
            return

        bk_author = select_author_by_id(bk_id)
        user_name = command.user_name

        if bk_author != user_name:
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


@check_login
def command_set_finish(command):
    """设置是否完结"""
    try:
        bk_name = command.params.get("bk_name")
        if is_any_blank(bk_name):
            return get_result(code=201, msg="参数不全")
        user_name = command.user_name
        bk_author = select_author_by_name(bk_name)

        if bk_author != user_name:
            return get_result(code=201, msg="无法修改")

        result = update_bk_status(bk_name, 1)
        if result:
            return get_result(code=200)
    except Exception, e:
        error_sen("command_set_finish", e)


@check_login
def command_my_chap(command):
    """查看我的章节"""
    try:
        page_index = command.params.get('page_index')
        bk_author = command.user_name
        bk_list = get_my_bk(bk_author)
        bk_ids = []
        for bk in bk_list:
            bk_ids.append(bk.get('bk_id'))
        bk_ids = list_to_str(bk_ids)
        chap_paging = get_my_cp(bk_ids, page_index)
        return get_result(code=200, data=chap_paging)
    except Exception, e:
        error_sen("command_my_chap", e)


@check_login
def command_search_chap(command):
    """查找我的章节"""
    try:
        cp_name = command.params.get('cp_name')
        if is_any_blank(cp_name):
            return
        bk_author = command.user_name
        bk_list = get_my_bk(bk_author)
        bk_ids = []
        for bk in bk_list:
            bk_ids.append(bk.get('bk_id'))
        bk_ids = list_to_str(bk_ids)
        chap_list = search_my_cp(cp_name, bk_ids)
        return get_result(code=200, data=chap_list)
    except Exception, e:
        error_sen("command_search_chap", e)


@check_login
def command_upload_txt(command):
    """上传整书"""
    try:
        bk_name = command.params.get("bk_name")
        bk_author = command.user_name
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
        cp_id = get_last_cp_id(bk_id)
        for i in range(1, chaps_num+1):
            cp_id += 1
            cp_content = txt[(i-1)*3000: i*3000]
            # 保存章节
            cp_words = len(cp_content)
            # 写入本地文件

            result_write = write_txt(get_string(cp_content), bk_id, cp_id)
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