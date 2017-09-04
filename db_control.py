# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sqlite3

# execute sql to create table
def createTable(c):
    create_table = '''create table if not exists users (name varchar(64),
                                                        mail varchar(32),
                                                        sbr  varchar(32))'''
    c.execute(create_table)

# execute sql to insert user
def insertUser(c, name, mail, sbrList):
    insertSql = 'insert into users (name, mail, sbr) values (?,?,?)'
    selectSql = 'select * from users where (name=? and mail=? and sbr=?)'

    for sbr in sbrList:

        c.execute(selectSql, (name, mail, sbr))
        entry = c.fetchone()

        if entry is not None:
            continue

        user = (name, mail, sbr)
        c.execute(insertSql, user)

def deleteUser(c, name, sbrList):
    deleteSql = 'delete from users where (name=? and sbr=?)'

    for sbr in sbrList:
        user = (name, sbr)
        c.execute(deleteSql, user)

def selectMailListBySBR(c, sbr):
    selectSql = 'select mail from users where sbr=?'
    
    rows=c.execute(selectSql, [sbr])

    mailList=[]
    for row in rows:
        mailList.append(str(row["mail"]))

    return mailList
