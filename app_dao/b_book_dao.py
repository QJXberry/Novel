# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_db import db_query_for_dict, db_query_for_list, db_query_for_paging, db_query_for_int, db_update,\
    db_insert, db_query_for_str, db_insert_lastrowid
import MySQLdb
from app_service.util_service import get_now_time


def find_bk_by_id(bk_id):
    sql = 'SELECT bk_name, bk_id, bk_author, bk_status, tp_id, bk_length, bk_lastdate, bk_abstract, ' \
          'bk_last_chap_name, bk_last_chap_id, bk_read_num FROM b_book where bk_id = %s'
    return db_query_for_dict(sql, bk_id)


def find_bk_name_lastchap_by_id(bk_id):
    sql = 'SELECT bk_name, bk_last_chap_id, tp_id FROM b_book WHERE bk_id = %s'
    return db_query_for_dict(sql, bk_id)


def search_books(name, page_index, page_size):
    """模糊查询"""
    name = MySQLdb.escape_string(name)
    sql = "FROM b_book WHERE bk_name like '%%%s%%' or bk_author like '%%%s%%'" % (name, name)
    return db_query_for_paging(sql, page_index, page_size,
                               fields="bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate",
                               order_by_field="bk_sort", order_by="DESC, bk_id")


def search_books_pc(name, num):
    """模糊查询"""
    name = MySQLdb.escape_string(name)
    sql = "SELECT bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_last_chap_name, bk_last_chap_id," \
          " bk_length FROM b_book WHERE bk_name like '%%%s%%' or bk_author" \
          " like '%%%s%%' LIMIT %s" % (name, name, num)
    return db_query_for_list(sql)


def select_by_tp(tp_ids, page_index, page_size):
    """通过ty_id查找"""
    sql = 'FROM b_book WHERE tp_id IN %s' % str(tp_ids)
    return db_query_for_paging(sql, page_index, page_size,
                               fields="bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_abstract",
                               order_by_field="bk_sort", order_by="DESC, bk_id")


def select_by_tp_pc(tp_ids, page_index, page_size):
    """PC分类页"""
    sql = 'FROM b_book WHERE tp_id IN %s' % str(tp_ids)
    return db_query_for_paging(sql, page_index, page_size,
                               fields="bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_last_chap_name,"
                                      " bk_last_chap_id, bk_length",
                               order_by_field="bk_sort", order_by="DESC, bk_id")


def select_wanjie_bk_pc(page_index, page_size):
    """PC分类已完结"""
    sql = 'FROM b_book WHERE bk_status = 1'
    return db_query_for_paging(sql, page_index, page_size,
                               fields="bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_last_chap_name,"
                                      " bk_last_chap_id, bk_length, bk_status ",
                               order_by_field="bk_sort", order_by="DESC, bk_id")


def select_original_bk_pc(page_index, page_size):
    """PC分类原创"""
    sql = 'FROM b_book WHERE bk_mark = 2'
    return db_query_for_paging(sql, page_index, page_size,
                               fields="bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_last_chap_name,"
                                      " bk_last_chap_id, bk_length, bk_status ",
                               order_by_field="bk_sort", order_by="DESC, bk_id")


def select_by_mark_sort(mark, page_index, page_size):
    """根据mark查询并按照bk_priority降序"""
    sql = "FROM b_book bk LEFT JOIN b_type tp on bk.tp_id = tp.tp_id WHERE bk_mark = %s"
    return db_query_for_paging(sql, page_index, page_size, args=mark, order_by_field="bk_priority")


def select_recom_bks(num):
    sql = "SELECT bk_id, bk_name, bk_author, bk_status, bk_lastdate, bk_abstract FROM b_book WHERE" \
          " bk_recom = 1 ORDER BY bk_sort DESC LIMIT %s" % num
    return db_query_for_list(sql)


def select_index_bks_by_tp(tp_ids, num=10):
    sql = "SELECT bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_abstract FROM b_book " \
          "WHERE tp_id in %s ORDER BY" \
          " bk_sort DESC LIMIT %s" % (str(tp_ids), num)
    return db_query_for_list(sql)


def select_index_bks_by_time():
    sql = "SELECT bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate FROM b_book ORDER BY" \
          " bk_lastdate DESC LIMIT 10"
    return db_query_for_list(sql)


def select_wanjie_bk(page_index, page_size):
    sql = 'FROM b_book WHERE bk_status = 1'
    return db_query_for_paging(sql, page_index, page_size,
                               fields="bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_abstract",
                               order_by_field="bk_sort", order_by="DESC, bk_id")


def select_paihang_bks(page_index, page_size):
    sql = 'FROM b_book'
    return db_query_for_paging(sql, page_index, page_size,
                               fields="bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_abstract",
                               order_by_field="bk_sort", order_by="DESC, bk_id")


def select_original_bks(page_index, page_size):
    sql = 'FROM b_book WHERE bk_mark = 2'
    return db_query_for_paging(sql, page_index, page_size,
                               fields="bk_id, bk_name, bk_author, bk_status, tp_id, bk_lastdate, bk_abstract",
                               order_by_field="bk_sort", order_by="DESC, bk_id")


def get_count_bks():
    sql = "SELECT count(*) FROM b_book"
    return db_query_for_int(sql)


def find_bk_id_url(bk_name):
    sql = "SELECT bk_id, original_url FROM b_book WHERE bk_name = %s"
    return db_query_for_dict(sql, bk_name)


def update_book_recom(bk_name, bk_recom):
    sql = "UPDATE b_book SET bk_recom = %s WHERE bk_name = %s"
    return db_update(sql, (bk_recom, bk_name))


def select_pic_bks(tp_ids, num):
    """PC首页有封面的"""
    sql = "SELECT bk_id, bk_name, bk_author, bk_length, bk_abstract FROM b_book WHERE" \
          " tp_id IN %s ORDER BY bk_sort DESC LIMIT %s"
    return db_query_for_list(sql, (tp_ids, num))


def select_pc_paihang_index(tp_ids, num):
    """PC首页排行榜"""
    sql = "SELECT bk_id, bk_name, bk_author FROM b_book WHERE tp_id IN %s ORDER BY bk_sort" \
          " DESC LIMIT %s"
    return db_query_for_list(sql, (tp_ids, num))


def select_pc_paihang_all(num):
    """PC首页总排行榜"""
    sql = "SELECT bk_id, bk_name, bk_author FROM b_book ORDER BY bk_sort" \
          " DESC LIMIT %s"
    return db_query_for_list(sql, num)


def get_recom_list():
    """小鸡推荐"""
    sql = "SELECT bk_id, bk_name, bk_sort FROM b_book WHERE bk_recom = 1 ORDER BY bk_sort DESC"
    return db_query_for_list(sql)


def change_recom_bk(bk_id, bk_recom):
    """修改小鸡推荐"""
    sql = "UPDATE b_book SET bk_recom = %s WHERE bk_id = %s"
    return db_update(sql, (bk_recom, bk_id))


def set_recom_bk(bk_name):
    """设置推荐"""
    sql = "UPDATE b_book SET bk_recom = 1 WHERE bk_name = %s"
    return db_update(sql, bk_name)


def get_recom_top_list():
    """查看优先级最高的前50本"""
    sql = "SELECT bk_id, bk_name, bk_sort FROM b_book ORDER BY bk_sort DESC LIMIT 50"
    return db_query_for_list(sql)


def update_sort(bk_sort, bk_name):
    sql = "UPDATE b_book SET bk_sort = %s WHERE bk_name = %s"
    return db_update(sql, (bk_sort, bk_name))


def select_pc_recom():
    """小鸡推荐"""
    sql = "SELECT bk_id, bk_name, bk_author FROM b_book WHERE bk_recom = 1 ORDER BY bk_sort DESC"
    return db_query_for_list(sql)


def add_new_bk(bk_name, bk_author, tp_id, bk_abstract):
    """作者新增小说"""
    bk_mark = 2
    bk_sort = 0
    sql = "INSERT INTO b_book(bk_name, bk_author, tp_id, bk_abstract, bk_mark, bk_sort, caiji_mark)" \
          " VALUES (%s, %s, %s, %s, %s, %s, 5)"
    return db_insert_lastrowid(sql, (bk_name, bk_author, tp_id, bk_abstract, bk_mark, bk_sort))


def get_my_bk(bk_author):
    """查看作者自己的书"""
    sql = "SELECT bk_id, bk_name FROM b_book WHERE bk_author = %s"
    return db_query_for_list(sql, bk_author)


def get_last_cp_id(bk_id):
    """获取最后一章的id"""
    sql = "SELECT bk_last_chap_id FROM b_book WHERE bk_id = %s"
    return db_query_for_int(sql, bk_id)


def update_author_bk(bk_id, bk_last_chap_name, bk_last_chap_id):
    """插入新章节后更书"""
    sql = "SELECT SUM(cp_words) FROM b_chapter WHERE bk_id = %s"
    bk_length = db_query_for_int(sql, bk_id)
    bk_length = (format(float(bk_length)/float(10000), '.2f'))
    bk_lastdate = get_now_time()
    sql = "UPDATE b_book SET bk_last_chap_name = %s, bk_last_chap_id = %s, bk_lastdate=%s, bk_length=%s" \
          " WHERE bk_id=%s"
    return db_update(sql, (bk_last_chap_name, bk_last_chap_id, bk_lastdate, bk_length, bk_id))


def update_bk_status(bk_name, bk_status):
    """设置连载或完结"""
    sql = "UPDATE b_book SET bk_status = %s WHERE bk_name = %s"
    return db_update(sql, (bk_status, bk_name))


def find_bk_by_name(bk_name):
    """查看这本书名存不存在"""
    sql = "SELECT bk_id FROM b_book WHERE bk_name = %s"
    return db_query_for_int(sql, bk_name)


def select_author_by_id(bk_id):
    """查看作者名称"""
    sql = "SELECT bk_author FROM b_book WHERE bk_id = %s"
    return db_query_for_str(sql, bk_id)


def select_author_by_name(bk_name):
    """查看作者名称"""
    sql = "SELECT bk_author FROM b_book WHERE bk_name = %s"
    return db_query_for_str(sql, bk_name)


def update_bk_read_num(bk_id):
    """阅读量+1"""
    sql = "UPDATE b_book SET bk_read_num = bk_read_num+1 WHERE bk_id = %s"
    return db_update(sql, bk_id)
