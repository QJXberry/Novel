# coding:utf8

from wheezy.captcha.image import curve, noise, text, offset, rotate, captcha, warp
from os import path
import random

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

_chars = '0123456789'


def create_captcha_number(count=4):
    return random.sample(_chars, count)


def create_captcha_image(code_list):
    try:
        font_file = path.join(
            path.dirname(path.abspath(__file__)), 'fonts', 'FreeSans.ttf'
        )
        captcha_image = captcha(drawings=[
            text(
                fonts=[font_file],
                font_sizes=[75],
                drawings=[
                    rotate(),
                    offset(dx_factor=0.3, dy_factor=0.2)
                ]
            ),
            curve(),
            noise()
        ])
        image = captcha_image(code_list)
        out = StringIO()
        image.save(out, "jpeg", quality=75)
        out = out.getvalue()
    except ImportError:
        out = None
        print 'captcha:', ''.join(code_list)
    return out

if __name__ == '__main__':
    print path.abspath(path.join('fonts', 'FreeSans.ttf'))
