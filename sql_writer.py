# -*- coding: utf-8 -*-
import sqlite3
import os
from func.log import logger


def sql_writer(db_name, func, auto, *argv):
    db_path = os.path.join('database', f'{db_name}.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if func == 'create':
        cmd = f'create table {db_name} '
        for arg in argv:
            cmd += arg
        # '(title varchar(100) primary key, last_update varchar(100), content varchar(1000))'
    elif func == 'insert':
        column_cursor = conn.execute(f'select * from {db_name}')
        columns = list(map(lambda x: x[0], column_cursor.description))
        cmd = f'insert into {db_name} ('
        if auto == True:
            columns = columns[1:]
        for idx, col in enumerate(columns):
            cmd += col
            if idx == len(columns) - 1:
                cmd += ') values ('
            else:
                cmd += ','
        for idx, arg in enumerate(argv):
            cmd += f'"{arg}"'
            if idx == len(argv) - 1:
                cmd += ')'
            else:
                cmd += ','
                
    try:
        cursor.execute(cmd)
    except Exception as e:
        print(e)
        logger.error(e)
    cursor.execute(f'select * from {db_name}')
    table = cursor.fetchall()
    print(table)
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # sql_writer('policies', 'create', '(title varchar(100) primary key, last_update varchar(100), content varchar(1000))')
    # sql_writer('policies', 'insert', '深圳核酸检测政策', '2021/6/26', '需提供72小时内的核酸证明，不需要隔离')
    # sql_writer('links', 'create', '(title varchar(100) primary key, last_update varchar(100), link varchar(1000))')
    # sql_writer('links', 'insert', '小红本和小黄本是什么?', '2021/6/25', 'https://mp.weixin.qq.com/s/UyYahnYirR49U_FO6N3HZg')
    # sql_writer('links', 'insert', '2021 TAMU CSSA 线上新生会来啦!', '2021/6/25', 'https://mp.weixin.qq.com/s/FSP3HsRTaNtd7sDGS62QLw')
    # sql_writer('google_flight', 'create', '(date varchar(100) primary key, url varchar(1000))')
    # sql_writer('google_flight', 'insert', '2021-08-20', 'https://www.google.com/travel/flights/search?tfs=CBwQAhoeagcIARIDSEtHEgoyMDIxLTA4LTIwcgcIARIDSUFIcAGCAQsI____________AUABSAGYAQI')
    # sql_writer('links', 'insert', 'Check Reporter', 'Up-to-date', 'https://www.checkee.info/')
    # sql_writer('events', 'create', '(id integer primary key autoincrement, title varchar(100), start_event datetime NOT NULL, end_event datetime NOT NULL, cost varchar(100))')
    sql_writer('events', 'insert', True, '坐船', '2021-08-20 12:00:00', '2021-08-20 14:00:00', '280￥'), 