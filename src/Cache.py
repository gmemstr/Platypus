# Completely rewritten with SQL in mind
import MySQLdb
import time
from src.Config import Config 

class Handler:
    def __init__(self):
        self.config = Config()
        #sqluser = self.config.Get("sql_user")
        #sqlpass = self.config.Get("sql_pass")
        #sqldb = self.config.Get("sql_db")
        
        sqluser = "root"
        sqlpass = ""
        sqldb = "platypus"

        self.db = MySQLdb.connect(user=sqluser,passwd=sqlpass,db=sqldb)
        self.c = self.db.cursor()

    def Get(self,server="all",offline="all"):
        if server == "all":
            self.c.execute("SELECT * FROM server")
            return self.c.fetchall()

    def SetStatus(self,panel,status,stats):
        self.c.execute("SELECT * FROM server WHERE id="+str(panel))
        udtime = self.c.fetchone()[5]
        if udtime >= 0 and status == "offline":
            # Server just went offline
            self.c.execute("UPDATE server SET online=false, udtime=0 WHERE id="+str(panel))
        elif udtime >= 0 and status == "online":
            # Increment uptime
            self.c.execute("UPDATE server SET udtime="+str(udtime + self.config.Get("scan_interval"))+" WHERE id="+str(panel))
        elif udtime <= 0 and status == "offline":
            # Deincrement uptime
            self.c.execute("UPDATE server SET udtime="+str(udtime - self.config.Get("scan_interval"))+" WHERE id="+str(panel))
        elif udtime <= 0 and status == "online":
            # Set reset uptime and set as online
            self.c.execute("UPDATE server SET online=true, udtime=0 WHERE id="+str(panel))
        self.db.commit()