import sqlite3
import sys
from model import Model
class Researchfocus(Model):
        def __init__(self):
             self.con=sqlite3.connect(self.db)
             self.cur=self.con.cursor()
             self.arr=[]
             self.arr.append(["""create table if not exists researchfocus(
             id integer primary key autoincrement,
             user_id integer,
             content text

             );""",[]])
             #self.con.commit()
             #self.con.close()
        def createmany(self, myid, mylist):
            #arr=[]
            for x in mylist:
                x["user_id"] = myid
                self.arr.append(["insert into researchfocus (user_id, content) values (:user_id, :content)",x])
                #self.con.commit()
            #self.con.close()
            return self.arr
        def updatemany(self, myid, mylist):
            ids=[myid]
            myvars=[]
            arr=[]
            for x in mylist:
                x["user_id"] = myid
                try:
                  ids.append(x["id"])
                  self.arr.append(["update researchfocus set content = :content where id = :id", x])
                  myvars.append("?")
                except:

                  self.arr.append(["insert into researchfocus (user_id, content) values (:user_id, :content)",x])
            if len(mylist) > 0:
                self.arr.insert(0,["delete from researchfocus where user_id = ? and id not in("+",".join(myvars)+")", ids])
                #self.con.commit()
            else:
                self.arr.insert(0,["delete from researchfocus where user_id = ?", ids])
                #self.con.commit()

            #self.con.close()
            return self.arr
