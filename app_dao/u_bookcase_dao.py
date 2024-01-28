# -*-coding:utf-8 -*-
from app_base.app_db import db_query_for_int, db_conn_guard, db_query_for_list, db_delete
from app_service.util_service import get_now_time
from app_base.app_log import error_sen


def add_book(u_id, bk_id, cp_id, cp_name):
    add_time = get_now_time()
    try:
        with db_conn_guard() as conn:
            sql = "SELECT id FROM u_bookcase WHERE u_id = %s AND bk_id = %s"
            case_id = conn.query_for_str(sql, (u_id, bk_id))
            if not case_id:
                sql = "INSERT INTO u_bookcase(u_id, bk_id, cp_id, add_time, cp_name) " \
                      "VALUES (%s, %s, %s, %s, %s)"
                conn.insert(sql, (u_id, bk_id, cp_id, add_time, cp_name))
            else:
                sql = "UPDATE u_bookcase SET cp_id = %s, add_time = %s, cp_name = %s " \
                      "WHERE u_id = %s AND bk_id = %s"
                conn.update(sql, (cp_id, add_time, cp_name, u_id, bk_id))
            result = conn.commit()
        return result
    except Exception, e:
        error_sen("add_book", e)


def count_user_bkcase(u_id):
    sql = "SELECT count(*) From u_bookcase WHERE u_id = %s"
    return db_query_for_int(sql, str(u_id), default=500)


def find_bk(u_id, bk_id):
    sql = "SELECT id FROM u_bookcase WHERE u_id = %s AND bk_id = %s"
    return db_query_for_int(sql, (u_id, bk_id))


def find_bk_case(u_id):
    sql = "SELECT c.bk_id, c.cp_name, c.cp_id, b.bk_name, b.bk_last_chap_name, b.bk_last_chap_id FROM u_bookcase c " \
          "LEFT JOIN b_book b on c.bk_id = b.bk_id WHERE c.u_id = %s "
    return db_query_for_list(sql, u_id)


def find_bk_case_pc(u_id):
    """书架"""
    sql = "SELECT c.bk_id, c.cp_name, c.cp_id, b.bk_name, b.bk_last_chap_name, b.bk_last_chap_id," \
          " b.bk_author, b.bk_lastdate, b.bk_status FROM u_bookcase c " \
          "LEFT JOIN b_book b on c.bk_id = b.bk_id WHERE c.u_id = %s "
    return db_query_for_list(sql, u_id)


def remove_bk_from_case(bk_id, u_id):
    sql = "DELETE FROM u_bookcase WHERE bk_id = %s and u_id = %s"
    return db_delete(sql, (bk_id, u_id))
