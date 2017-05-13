import socket
import MySQLdb

db = MySQLdb.connect(user="root", db="platypus")
c = db.cursor()

c.execute("SELECT * FROM server")
dbdata = c.fetchall()

for server in dbdata:
    ip = socket.gethostbyname(server[2])
    c.execute("UPDATE server SET IP=%s where id=%s", (ip, server[0]))
    db.commit()

print("Done")
