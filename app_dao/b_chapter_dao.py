# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
import MySQLdb
from app_base.app_lru import lru_cache_function

from app_base.app_db import db_query_for_list, db_query_for_dict, db_query_for_int, db_insert, db_update, \
    db_query_for_paging


def find_cp_name_by_bk(bk_id):
    sql = 'SELECT cp_id, cp_name, cp_warn FROM b_chapter where bk_id = %s order by cp_id desc'
    return db_query_for_list(sql, bk_id)


def find_cp_by_id(cp_id, bk_id):
    sql = 'SELECT cp_name, cp_words FROM b_chapter where cp_id = %s and bk_id =%s'
    return db_query_for_dict(sql, (cp_id, bk_id))


@lru_cache_function(expiration=60*60)
def get_count_cps():
    """总章节数"""
    sql = "SELECT count(*) FROM b_chapter"
    return db_query_for_int(sql)


def add_chap(bk_id, cp_name, cp_id, cp_words):
    sql = "INSERT INTO b_chapter(bk_id, cp_name, cp_id, cp_words) VALUES (%s, %s, %s, %s)"
    return db_insert(sql, (bk_id, cp_name, cp_id, cp_words))


def update_chap(bk_id, cp_name, cp_id, cp_words):
    """更新章节"""
    sql = "UPDATE b_chapter SET cp_name = %s, cp_words = %s WHERE bk_id = %s and cp_id = %s"
    return db_update(sql, (cp_name, cp_words, bk_id, cp_id))


def get_my_cp(bk_ids, page_index):
    """分页获取作者的章节列表"""
    sql = "FROM b_chapter c LEFT JOIN b_book b on c.bk_id = b.bk_id" \
          " WHERE b.bk_id IN %s" % bk_ids
    return db_query_for_paging(sql, page_index, 10, fields="c.bk_id, b.bk_name, cp_id, cp_name ")


def search_my_cp(cp_name, bk_ids):
    """模糊查询章节"""
    cp_name = MySQLdb.escape_string(cp_name)
    sql = "SELECT c.bk_id, b.bk_name, cp_id, cp_name FROM b_chapter c LEFT JOIN b_book b on c.bk_id = b.bk_id" \
          " WHERE b.bk_id IN %s AND cp_name LIKE '%%%s%%'" % (bk_ids, cp_name)
    return db_query_for_list(sql)
