# -*-coding:utf-8 -*-
from tornado.web import RequestHandler
from app_base.app_captcha import create_captcha_number, create_captcha_image
from app_base.app_lru import lru_cache_function

import time
from app_base.app_log import error_sen


class CaptchaHandler(RequestHandler):
    def get(self, *args, **kwargs):
        captcha_image = ''
        try:
            code_list = create_captcha_number(4)
            captcha_image = _create_captcha_image(code_list)
            # 保存生成的验证码，需要验证时取出验证, 验证码有效时间为5分钟
            code = "".join(code_list)
            self.set_secure_cookie("code", code, expires=time.time() + 60 * 5)
            if captcha_image:
                self.set_header('content-type', 'image/jpeg')
                self.write(captcha_image)
        except Exception, e:
            error_sen("CaptchaHandler", e)


@lru_cache_function(expiration=60*60)
def _create_captcha_image(code_list):
    return create_captcha_image(code_list)
