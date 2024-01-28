# -*-coding:utf-8 -*-
from app_base.app_db import db_insert, db_query_for_list, db_delete
"""友情连接dao"""


def insert_link(link_name, link_address, link_sort):
    sql = "INSERT INTO l_link(link_name, link_address, link_sort) VALUES (%s, %s, %s) "
    return db_insert(sql, (link_name, link_address, link_sort))


def get_link_list():
    sql = "SELECT * FROM l_link"
    return db_query_for_list(sql)


def del_link(id):
    sql = "DELETE FROM l_link WHERE id = %s"
    return db_delete(sql, id)