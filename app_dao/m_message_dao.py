# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_db import db_insert, db_query_for_int, db_query_for_paging, db_query_for_dict, db_update
import time


def inset_msg(u_id, user_name, msg_name, msg_phone, msg_cont, msg_ip):
    msg_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    sql = "INSERT INTO m_message(u_id, user_name, msg_name, msg_phone, msg_cont, msg_ip, msg_time) VALUES" \
          " (%s, %s, %s, %s, %s, %s, %s)"
    return db_insert(sql, (u_id, user_name, msg_name, msg_phone, msg_cont, msg_ip, msg_time))


def get_count_msg():
    sql = "SELECT count(*) FROM m_message"
    return db_query_for_int(sql)


def get_msg_paging(page_index):
    sql = "from m_message where admin_reply=0 order by m_id asc"
    return db_query_for_paging(sql, page_index, 10)


def inset_reply_msg(u_id, msg_cont, msg_ip):
    msg_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    sql = "INSERT INTO m_message(u_id, msg_cont, msg_ip, msg_time, admin_reply) VALUES" \
          " (%s, %s, %s, %s, %s)"
    return db_insert(sql, (u_id, msg_cont, msg_ip, msg_time, 1))


def check_admin_reply(u_id):
    sql = "SELECT msg_cont, m_id FROM m_message WHERE u_id = %s AND admin_reply=1 LIMIT 1"
    msg = db_query_for_dict(sql, u_id)

    if msg:
        m_id = msg.get('m_id')
        sql = "UPDATE m_message SET admin_reply=2 WHERE m_id=%s"
        re = db_update(sql, m_id)
        return msg.get('msg_cont')


if __name__ == '__main__':
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))