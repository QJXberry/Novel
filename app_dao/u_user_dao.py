# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_db import db_query_for_int, db_insert_lastrowid, db_query_for_list, db_delete, db_query_for_paging
from app_base.app_db import db_query_for_dict


def find_id_by_user_name(user_name):
    sql = "SELECT u_id FROM u_user WHERE user_name = %s"
    return db_query_for_int(sql, user_name)


def insert_user(user_name, password, reg_ip, reg_time, device, u_type):
    sql = "INSERT INTO u_user(user_name, password, reg_ip, reg_time, device, u_type) " \
          "VALUES (%s, %s, %s, %s, %s, %s) "
    return db_insert_lastrowid(sql, (user_name, password, reg_ip, reg_time, device, u_type))


def find_id_by_name_pwd(user_name, password):
    sql = "SELECT u_id FROM u_user WHERE user_name = %s and password = %s"
    return db_query_for_int(sql, (user_name, password))


def find_id_type_by_name_pwd(user_name, password):
    sql = "SELECT u_id, u_type FROM u_user WHERE user_name = %s and password = %s"
    return db_query_for_dict(sql, (user_name, password))


def get_count_users():
    sql = "SELECT count(*) FROM u_user"
    return db_query_for_int(sql)


def del_user(u_id):
    """删除用户"""
    sql = "DELETE FROM u_user WHERE u_id = %s"
    return db_delete(sql, u_id)


def get_user_list_paging(page_index):
    sql = "FROM u_user ORDER BY u_id DESC"
    return db_query_for_paging(sql, page_index, 10)