# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
from app_base.app_db import db_query_for_list


def select_module_navigation(m_name):
    sql = "SELECT * FROM i_navigation n LEFT JOIN i_module m on n.m_id = m.m_id where m_name = %s" \
          " ORDER BY sm_priority ASC"
    return db_query_for_list(sql, m_name)


if __name__ == '__main__':
    from app_base.app_log import enable_pretty_logging
    enable_pretty_logging(options=None)
    print select_module_navigation("m_class")
