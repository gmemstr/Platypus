import socket
import MySQLdb

db = MySQLdb.connect(user="root", db="platypus")
c = db.cursor()

c.execute("SELECT * FROM server")
dbdata = c.fetchall()

for server in dbdata:
    ip = socket.gethostbyname(server[2])
    print(server[0], server[1], ip)

print("Done")
