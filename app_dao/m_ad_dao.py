# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_db import db_insert, db_query_for_list, db_delete
"""广告dao"""


def get_ad_list():
    sql = "SELECT * FROM m_ad"
    return db_query_for_list(sql)


def del_ad(id):
    sql = "DELETE FROM m_ad WHERE id = %s"
    return db_delete(sql, id)


def insert_ad(ad_description, ad_url, file_name):
    sql = "INSERT INTO m_ad(ad_description, ad_url, file_name) VALUES (%s, %s, %s) "
    return db_insert(sql, (ad_description, ad_url, file_name))
