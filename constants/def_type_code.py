# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'


def get_tp_name_m(tp_id):
    return get_tp_name_pc(get_class_id(tp_id))


def get_tp_name_pc(tp_id):
    if tp_id == 1:  # 1
        return "热门小说"
    if tp_id == 2:  # 2
        return "热追现言"
    if tp_id == 3:  # 3
        return "热追古言"
    if tp_id == 4:  # 4
        return "热追幻言"
    if tp_id == 5:  # 5
        return "热门男频"
    if tp_id == 6:  # 6
        return "热读纯爱"
    if tp_id == 98:
        return "精品书库"
    if tp_id == 99:
        return "完结书库"
    if tp_id == 100:
        return "总排行"
    return ""


def get_class_id(tp_id):
    if tp_id in (20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34):  # 1
        return 1
    if tp_id in (22, 30):  # 2
        return 2
    if tp_id in (23, 29):  # 3
        return 3
    if tp_id in (24, 25, 26, 27, 31, 32, 33):  # 4
        return 4
    if tp_id in (20, 21, 24, 25, 26, 28, 31, 32, 33):  # 5
        return 5
    if tp_id in (34,):  # 6
        return 6


def get_type_id_m(tp_id):
    if tp_id == 1:
        return 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34
    if tp_id == 2:
        return 22, 30
    if tp_id == 3:
        return 23, 29
    if tp_id == 4:
        return 24, 25, 26, 27, 31, 32, 33
    if tp_id == 5:
        return 20, 21, 24, 25, 26, 28, 31, 32, 33
    if tp_id == 6:
        return 34, 34
    # 非法
    return 0


def get_tp_name(id):
    if id == 20:
        return "玄幻魔法"
    if id == 21:
        return "仙侠修真"
    if id == 22:
        return "都市言情"
    if id == 23:
        return "历史军事"
    if id == 24:
        return "网游竞技"
    if id == 25:
        return "科幻灵异"
    if id == 26:
        return "恐怖惊悚"
    if id == 27:
        return "其他类型"
    if id == 28:
        return "武侠修真"
    if id == 29:
        return "穿越历史"
    if id == 30:
        return "青春校园"
    if id == 31:
        return "网游动漫"
    if id == 32:
        return "科幻空间"
    if id == 33:
        return "恐怖灵异"
    if id == 34:
        return "耽美同人"


SORT_ALL = 100  # 总排行

SORT_FINISHED = 99  # 完结

SORT_ORIGINAL = 98  # 原创

if __name__ == '__main__':
    print get_type_id_m(1)

