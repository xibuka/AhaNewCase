#!/usr/bin/python3

import db_control
import sqlite3
import argparse

dbname = '/etc/freshcase/ecs.db'

# get the arguments from command line                     
parser = argparse.ArgumentParser()                        
parser.add_argument("--name",  \
                help="your name")                  
parser.add_argument("--mail",  \
                help="send to mail address.")                  
parser.add_argument("--sbr",\
                help="specify sbr plate you want to check. \
                      mush be one of 'gluster', 'stack', 'ceph', 'cloudform'")  
parser.add_argument("--action",\
                help="add ,remove or show entry. \
                      mush be one of 'add', 'remove', 'show'")  
args = parser.parse_args()                                
args = vars(args)                                         

name   =args['name']
mail   =args['mail']
sbr    =args['sbr']
action =args['action']

if sbr not in ["gluster", "stack", "ceph", "cloudform"]:
    print('wrong sbr! must be one of "gluster" "stack" "ceph" "cloudform"')
    exit(1)

conn = sqlite3.connect(dbname)
#conn.row_factory = sqlite3.Row
c = conn.cursor()

if action == "add":
    db_control.insertUser(c, name, mail, [sbr])
    conn.commit()
elif action == "remove":
    db_control.deleteUser(c, name, [sbr])
    conn.commit()
elif action == "show":
    select_sql = 'select * from users where name=?'
    for row in c.execute(select_sql, [name]):
        print(row)
else:
    print('wrong action, must be one of "add",  "remove", "show"')

conn.close()

