import db_control
import sqlite3

dbname = 'ecs.db'

conn = sqlite3.connect(dbname)
#conn.row_factory = lambda cursor, row: row[0]
conn.row_factory = sqlite3.Row
c = conn.cursor()

db_control.createTable(c)
db_control.insertUser(c, "wenhan", "wenshi@redhat.com", ["gluster", "stack", "ceph", "cloudform"])
db_control.insertUser(c, "wenhan", "shibunkan@gmail.com", ["gluster", "stack", "ceph", "cloudform"])

conn.commit()

select_sql = 'select * from users'
for row in c.execute(select_sql):
    print(row)

conn.close()

