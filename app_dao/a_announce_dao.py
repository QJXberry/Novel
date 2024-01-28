# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_db import db_query_for_list, db_delete, db_insert


def get_announce_list():
    sql = "SELECT * FROM a_announcement"
    return db_query_for_list(sql)


def del_announce(a_id):
    sql = "DELETE FROM a_announcement WHERE a_id = %s"
    return db_delete(sql, a_id)


def insert_announce(a_announce, sort, red):
    sql = "INSERT INTO a_announcement(a_announce, sort, red)  VALUES (%s, %s, %s)"
    return db_insert(sql, (a_announce, sort, red))
