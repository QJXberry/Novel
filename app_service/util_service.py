# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
import os
from settings import TXT_BASE_PATH, BASE_DIR
from app_base.app_log import error_sen, info_sen
import time

import re
import datetime
import requests
import socket

import struct
from random import randint
from settings import PIC_PATH, TXT_BASE_PATH
import types


def get_cp_cont(bk_id, cp_id):
    try:
        path = TXT_BASE_PATH + '/' + str(bk_id) + '/' + str(cp_id) + '.txt'
        if not os.path.exists(path):
            return False
        cp = open(path, 'r')
        cp_cont = cp.read()
        cp.close()
        return cp_cont
    except Exception, e:
        print "get_cp_cont ERROR:", str(e)


def write_html(html, file_name, file_dir):
    """生成静态"""
    try:
        path = BASE_DIR + '/web/template/' + file_dir + '/' + file_name + '.html'
        file_object = open(path, 'w')
        file_object.write(html)
        return True
    except Exception, e:
        print "write_html ERROR:", str(e)
        return False
    finally:
        file_object.close()


def get_now_time():
    """获取当前时间"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def delete_tag(s):
    if not s:
        return ''
    dr = re.compile(r'<[^>]*?>', re.S)
    return dr.sub('', s)


def get_time_tip():
    tip = ""
    i = datetime.datetime.now()
    h = i.hour
    m = i.minute
    if 0 <= h <= 5:
        tip = "<h4>&nbsp;&nbsp;&nbsp;&nbsp;小鸡时间%s点%s分，该睡觉了！</h4><br/>" % (h, m)
    return tip


def get_html(url, charset="utf-8", interval=None):
    """interval 间隔时间 单位S"""
    try:
        html = ""
        for i in range(5):
            html = _get_html_request(url, charset, interval)
            if html:
                break
        return html
    except Exception, e:
        error_sen("get_html", e)


def _get_html_request(url, charset, interval=None):
    """fail: 0"""
    try:
        if interval:
            time.sleep(interval)
        req = requests.session()
        req.keep_alive = False
        user_agent = _create_user_agent()
        headers = {'User-Agent': user_agent,  "Connection": "close", "X-Forwarded-For": _get_random_ip()}
        html = req.get(url, headers=headers, timeout=15)
        html.encoding = charset
        html = html.text
        return html
    except requests.exceptions.Timeout, e:
        info_sen("_get_html_request 超时", e, url=url)
        return 0
    except Exception, e:
        info_sen("_get_html_request", e, url=url)
        return 0


def _create_user_agent():
    agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 ",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) ",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122",
        "Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
    ]
    num = randint(0, len(agent_list) - 1)
    return agent_list[num]


def _get_random_ip():
    return socket.inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))


def download_img(url, bk_id):
    try:
        bk_id = str(bk_id)
        user_agent = _create_user_agent()
        headers = {'User-Agent': user_agent, "Connection": "close"}
        response = requests.get(url, stream=True, headers=headers)
        img = response.content
        pic_path = PIC_PATH + '/' + bk_id + '.jpg'
        with open(pic_path, "wb") as pic:
            pic.write(img)
        return True
    except Exception, e:
        error_sen("download_img", e)


def write_txt(cont, bk_id, cp_id):
    """success: 1, fail: 0"""
    try:
        if not cont:
            return 1
        # linux文件锁删除了
        bk_id = str(bk_id)
        cp_id = str(cp_id)
        file_path = TXT_BASE_PATH + '/' + bk_id
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        txt_path = file_path + '/' + cp_id + '.txt'
        with open(txt_path, 'w') as file_object:
            file_object.write(cont)
            return 1
    except Exception, e:
        error_sen("write_txt", e)
        return 0


def list_to_str(list):
    string = str(tuple(list))
    if len(list) == 1:
        string = string[:-2] + ')'
    return string





class NotIntegerError(Exception):
    pass


class OutOfRangeError(Exception):
    pass


_MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九',)
_P0 = (u'', u'十', u'百', u'千',)
_S4, _S8, _S16 = 10 ** 4, 10 ** 8, 10 ** 16
_MIN, _MAX = 0, 9999999999999999


def _to_chinese4(num):
    '''转换[0, 10000)之间的阿拉伯数字
    '''
    assert (0 <= num and num < _S4)
    if num < 10:
        return _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = u''

        for idx, val in enumerate(lst):
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'零'

        return result[::-1].replace(u'一十', u'十')


def _to_chinese8(num):
    assert (num < _S8)
    to4 = _to_chinese4
    if num < _S4:
        return to4(num)
    else:
        mod = _S4
        high, low = num / mod, num % mod
        if low == 0:
            return to4(high) + u'万'
        else:
            if low < _S4 / 10:
                return to4(high) + u'万零' + to4(low)
            else:
                return to4(high) + u'万' + to4(low)


def _to_chinese16(num):
    assert (num < _S16)
    to8 = _to_chinese8
    mod = _S8
    high, low = num / mod, num % mod
    if low == 0:
        return to8(high) + u'亿'
    else:
        if low < _S8 / 10:
            return to8(high) + u'亿零' + to8(low)
        else:
            return to8(high) + u'亿' + to8(low)


def num_to_chinese(num):
    if type(num) != types.IntType and type(num) != types.LongType:
        raise NotIntegerError(u'%s is not a integer.' % num)
    if num < _MIN or num > _MAX:
        raise OutOfRangeError(u'%d out of range[%d, %d)' % (num, _MIN, _MAX))

    if num < _S4:
        return _to_chinese4(num)
    elif num < _S8:
        return _to_chinese8(num)
    else:
        return _to_chinese16(num)


if __name__ == '__main__':
    print num_to_chinese(123)