import asyncio
import MySQLdb
from src.Config import Config

class Sql:
    def __init__(self):
        self.Config = Config()

        self.config = Config()
        self.sqluser = self.config.Get("sql_user")
        self.sqlpass = self.config.Get("sql_pass")
        self.sqltable = self.config.Get("sql_db")

        self.db = MySQLdb.connect(user=self.sqluser,passwd=self.sqlpass,db="platypus")
        self.c = self.db.cursor()

    def CheckConnection(self):
        try:
            self.db.ping()
        except:
            self.db =  MySQLdb.connect(user=self.sqluser,passwd=self.sqlpass,db="platypus")

    def Get(self,filter=None,arg=None):
        self.CheckConnection()
        if filter == None:
            self.c.execute("SELECT * FROM " + self.sqltable)
            yield self.c.fetchall()
        if filter == "one":
            self.c.execute("SELECT * FROM " + self.sqltable + " WHERE id=%s", (arg))
            yield self.c.fetchall()
        else:
            raise ValueError('Invalid filter for SQL query')

    def Set(self,panel,online,cpu,memory,disk):
        self.CheckConnection()
        self.c.execute("UPDATE " + self.sqltable + " SET online=%s,cpu=%s,memory=%s,disk=%s WHERE id=%s",
                        (online, cpu, memory, disk, panel))

    def RemoveServer(self, panel):
        self.CheckConnection()

        self.c.execute("DELETE FROM "+self.sqltable+" WHERE id="+str(panel))
        self.db.commit()
        return True
    def CreateServer(self, panel, form):
        self.CheckConnection()
        
        # Insert new server into database
        self.c.execute("INSERT INTO " + self.sqltable + " (id,name,hostname,location) VALUES (%s,%s,%s,%s)",
            (int(form['id']),form['name'],form['hostname'],form['location']))
        self.db.commit()
        return True
    def ModServer(self, panel, form):
        self.CheckConnection()
        
        # Edit server
        self.c.execute("UPDATE " + self.sqltable + " SET name=%s,hostname=%s WHERE id=%s",
            (form['name'], form['hostname'], panel))
        self.db.commit()
        return True

    def GetAsJson(self,panel):
        raw = self.Get("one",panel)
        res = {}
        for s in raw:
            print(s)
            res[s[0]] = {"name": s[1],
                      "online": s[4],
                      "location": s[3],
                      "cpu": s[6],
                      "memory":s[7],
                      "disk":s[8]}
        return res