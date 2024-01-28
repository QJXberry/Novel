# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from tornado.web import RequestHandler
from app_dao.b_book_dao import find_bk_name_lastchap_by_id
from app_dao.b_chapter_dao import find_cp_by_id

from app_service.util_service import get_cp_cont, get_time_tip
from app_service.common_service import get_next_id, get_pre_id

from app_handler.util_handler import reject_ip, get_referer
from random import randint
from constants.def_msg import MSG1, MSG2


class MobileChapHandler(RequestHandler):
    def get(self,  *args, **kwargs):
        bk_id = args[0]
        cp_id = int(args[1])
        bk = find_bk_name_lastchap_by_id(bk_id)
        if bk:
            bk_name = bk.get("bk_name")
            bk_last_chap_id = bk.get("bk_last_chap_id")
            process = cp_id * 100 / bk_last_chap_id
            chap = find_cp_by_id(cp_id, bk_id)
            cp_cont = get_cp_cont(bk_id, cp_id)
            if not cp_cont:
                if cp_id > bk_last_chap_id:
                    self.redirect("/m/%s/%s" % (bk_id, bk_last_chap_id))
                    return
                else:
                    cp_cont = MSG1
                    chap['cp_name'] = chap.get("cp_name") or MSG2
                    chap['cp_words'] = "0"
            pre_id = get_pre_id(cp_id)
            next_id = get_next_id(bk_last_chap_id, cp_id)
            referer = get_referer(self)
            time_tip = get_time_tip()
            self.render('bk_mobile/chapter.html', bk_name=bk_name, chap=chap, cp_cont=cp_cont, pre_id=pre_id,
                        next_id=next_id, bk_id=bk_id, cp_id=cp_id, randint=randint(1, 3), referer=referer,
                        time_tip=time_tip, process=process)
        else:
            # 没有这本书, 封ip
            reject_ip(self)
            pass

    def data_received(self, chunk):
        pass


if __name__ == '__main__':
    print randint(0, 2)
