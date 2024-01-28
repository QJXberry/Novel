# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_log import error_sen
from app_base.app_db import db_query_for_list, db_delete, db_query_for_str, db_update
import shutil

from settings import TXT_BASE_PATH
from app_dao.b_book_dao import find_bk_id_url
from app_service.util_service import download_img
import os


def delete_repeat_bks():
    try:
        # 查找重复章节的书的id
        sql = "select bk_id from b_chapter GROUP BY cp_name, cp_url having count(*)>1"
        result_list = db_query_for_list(sql)
        if not result_list:
            return True
        bk_id_list = []
        for r in result_list:
            bk_id = r.get("bk_id")
            if bk_id not in bk_id_list:
                bk_id_list.append(bk_id)
        print bk_id_list
        # 删除文件夹
        for bk_id in bk_id_list:
            file_path = TXT_BASE_PATH + '/' + str(bk_id)
            shutil.rmtree(file_path)

        # 删除chapter表
        for bk_id in bk_id_list:
            sql = "DELETE FROM b_chapter WHERE bk_id = %s"
            result = db_delete(sql, bk_id)
            if not result:
                error_sen("删除重复章节失败", sql)

        # 删除book 表
        for bk_id in bk_id_list:
            sql = "DELETE FROM b_book WHERE bk_id = %s"
            result = db_delete(sql, bk_id)
            if not result:
                error_sen("删除重复的书失败", sql)

        # 修改b_target表
        for bk_id in bk_id_list:
            sql = "SELECT bk_name FROM b_book WHERE bk_id = %s"
            bk_name = db_query_for_str(sql, bk_id)
            if bk_name:
                sql = "UPDATE b_target SET target_mark = 15 WHERE bk_name = %s"
                result = db_update(sql, bk_name)
                if not result:
                    error_sen("更新b_target失败", sql)
    except Exception, e:
        error_sen("delete_repeat_bks", e)


def change_pic(bk_name, pic_num=1):
    try:
        bk = find_bk_id_url(bk_name)
        if pic_num == 1:
            pic_num = "180"
        else:
            pic_num = "300"
        if not bk:
            return False
        bk_id = bk.get("bk_id")
        original_url = bk.get("original_url")
        original_bk_id = original_url.split('/')[-1]
        pic_url = "http://qidian.qpic.cn/qdbimg/349573/%s/%s" % (original_bk_id, pic_num)
        print pic_url
        result = download_img(pic_url, bk_id)
        return result
    except Exception, e:
        error_sen("change_pic", e, bk_name=bk_name)


def del_bk(bk_id):
    """删除整本书"""
    try:
        # 删除TXT文件夹
        file_path = TXT_BASE_PATH + '/' + str(bk_id)
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
        # 删除chapter表
        sql = "DELETE FROM b_chapter WHERE bk_id = %s"
        result = db_delete(sql, bk_id)

        # 删除book 表
        sql = "DELETE FROM b_book WHERE bk_id = %s"
        result = db_delete(sql, bk_id)
        return True
    except Exception, e:
        error_sen("del_bk", e, bk_id=bk_id)
        return "系统错误" + str(e)


def del_cp(bk_id, cp_id):
    try:
        """删除txt文件"""
        file_name = TXT_BASE_PATH + '/' + str(bk_id) + '/' + str(cp_id) + ".txt"
        if os.path.exists(file_name):
            os.remove(file_name)
        return True
    except Exception, e:
        error_sen("del_cp", e)

