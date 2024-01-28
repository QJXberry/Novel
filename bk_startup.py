# coding:utf8
import sys
from os import path

import gevent.pywsgi
from gevent import monkey

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options, define
from tornado.web import Application
from tornado.wsgi import WSGIApplication

from app_base.app_log import enable_pretty_logging, logging
from app_handler.admin_handler import admin_handler
from app_handler.admin_handler import admin_handler_login, admin_handler_dynamic
from app_handler.admin_handler.base_m_handler import get_post_command_dict
from app_handler.base_handler import ErrorHandler

from app_handler.handler_captcha import CaptchaHandler
from app_handler.mobile_handler import m_handler_index, m_handler_bk, m_handler_chap, m_handler_search,\
    m_handler_class, m_handler_login, m_handler_register, m_handler_contact,\
    m_handler_bookcase
from app_handler.pc_handler import pc_handler_index, pc_handler_bk, pc_handler_chap, pc_handler_login, \
    pc_handler_class, pc_handler_register, pc_handler_bookcase, pc_handler_add, pc_handler_contact, pc_handler_search

from app_handler.writer_handler import writer_handler_login, writer_handler
from settings import DEBUG_PROJECT, BASE_DIR
monkey.patch_all()

define(name='port', default=8888, type=int, help='run on the given port')
"""
+: 一次或多次
?: 0或1次
*: 0或多
"""


def get_application():
    kwargs = dict(
        handlers=[
            # 手机端
            (r'.*/captcha$', CaptchaHandler),  # 验证码
            (r'^/m(/)?(index)?(.html)?$', m_handler_index.MobileIndexHandler),  # 首页
            (r'^/m/(\d+)(.html)?$', m_handler_bk.MobileBkHandler),  # 小说
            (r'^/m/(\d+)/(\d+)(.html)?$', m_handler_chap.MobileChapHandler),  # 章节
            (r'^/m/class/(\d+)/(\d+)(.html)?$', m_handler_class.MobileClassHandler),  # 分类
            (r'^/m/search(.html)?$', m_handler_search.MobileSearchHandler),  # 查找
            (r'^/m/contact(.html)?$', m_handler_contact.MobileContactHandler),  # 联系小鸡
            (r'^/m/register(.html)?$', m_handler_register.MobileRegisterHandler),  # 注册
            (r'^/m/login(.html)?$', m_handler_login.MobileLoginHandler),  # 登入
            (r'^/m/add$', pc_handler_add.PcAddHandler),  # 添加书签
            (r'^/m/bookcase$', m_handler_bookcase.MobileBookcaseHandler),  # 访问书架, 删除书架书籍

            # PC端
            (r'^/pc(/)?(index)?$', pc_handler_index.PcIndexHandler),  # 首页
            (r'^/pc/(\d+)(.html)?$', pc_handler_bk.PcBkHandler),  # 书目录
            (r'^/pc/(\d+)/(\d+)(.html)?$', pc_handler_chap.PcChapHandler),  # 章节
            (r'^/pc/class/(\d+)/(\d+)(.html)?$', pc_handler_class.PcClassHandler),  # 分类
            (r'^/pc/login(.html)?$', pc_handler_login.PcLoginHandler),  # 登入
            (r'^/pc/register(.html)?$', pc_handler_register.PcRegisterHandler),  # 注册
            (r'^/pc/bookcase$', pc_handler_bookcase.PcBookcaseHandler),  # 访问书架, 删除书架书籍
            (r'^/pc/add$', pc_handler_add.PcAddHandler),  # 访问书架, 删除书架书籍
            (r'^/pc/search(.html)?$', pc_handler_search.PcSearchHandler),  # 查找
            (r'^/pc/contact(.html)?$', pc_handler_contact.PcContactHandler),  # 联系小鸡
            # 管理后台
            (r'^/sengo/xhj/(\w+)$', admin_handler.AdminHandler, dict(
                command_dict=get_post_command_dict(admin_handler))),
            (r'^/sengo/login$', admin_handler_login.AdminLoginHandler),
            (r'^/sengo/xhj/dynamic/(\w+)$', admin_handler_dynamic.AdminDynamicHandler, dict(
                command_dict=get_post_command_dict(admin_handler_dynamic))),  # 生成静态
            # 作者
            (r'^/writer/login$', writer_handler_login.WriterLoginHandler),
            (r'^/writer/(\w+)$', writer_handler.WriterHandler, dict(
                command_dict=get_post_command_dict(writer_handler))),
            (r'/.*$', ErrorHandler)
        ],
        template_path=path.join(BASE_DIR, 'web/template'),
        static_path=path.join(BASE_DIR, 'web/static'),
        cookie_secret='C4+ZSGiq/gRm06wcOo=',
        debug=DEBUG_PROJECT,
        # xsrf_cookies=True
    )
    if DEBUG_PROJECT:
        return Application(**kwargs)
    else:
        return WSGIApplication(**kwargs)


options.parse_command_line()
log_options = dict(
    log_level='WARN',
    log_to_stderr=True,
    log_dir=path.join(BASE_DIR, 'log'),
    log_file_prefix='bk_xhj_',
    log_file_postfix='.log',
    log_file_num_backups=20
)
enable_pretty_logging(options=log_options)

application = get_application()


def startup():
    reload(sys)
    sys.setdefaultencoding('gbk')
    print 'startup game bk_xhj %s...' % options.port

    if DEBUG_PROJECT:
        http_server = HTTPServer(application, xheaders=True)
        http_server.listen(options.port)
        IOLoop().instance().start()
    else:
        gevent.pywsgi.WSGIServer(('', options.port), application, log=None,
                                 error_log=logging.getLogger()).serve_forever()


if __name__ == '__main__':
    startup()
    