# coding:utf8
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG_PROJECT = True
DB_CONN_NUM = 5

DB_KWARGS = dict(
    host='127.0.0.1',
    port=8847,
    user='root',
    passwd='mima543',
    db='db_novel',
    charset="utf8"
)
"""
DB_KWARGS = dict(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='mima543',
    db='db_novel',
    charset="utf8"
)
"""

REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
    'password': None,
    'expire': 7*24*60*60,
}

TXT_BASE_PATH = 'E:' + '/' + 'txt'
'''
TXT_BASE_PATH = '/home/sengo/Pictures/bk/txt'
'''

PIC_PATH = 'E:' + '/' + 'pic'

AD_PATH = 'E:/new'

PAGE_SIZE = 10

PC_PAGE_SIZE = 15

SEARCH_RATE = 10  # 单位s ,间隔多少s能继续搜索

REG_RATE = 60*60

IPS_LENGTH = -2

BK_NUM_LIMIT = 10  # 书架上限

