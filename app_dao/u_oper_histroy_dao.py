# -*-coding:utf-8 -*-
from app_base.app_db import db_insert


def insert_oper_histroy(u_id, ip, device, oper_cont, oper_time):
    sql = "INSERT INTO u_oper_histroy(u_id, ip, device, oper_cont, oper_time) VALUES (%s, %s, %s, %s, %s)"
    return db_insert(sql, (u_id, ip, device, oper_cont, oper_time))

