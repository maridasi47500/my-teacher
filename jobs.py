import sqlite3
import sys
from model import Model
class Jobs(Model):
        def __init__(self):
             #self.con=sqlite3.connect(self.db)
             #self.cur=self.con.cursor()
             self.arr=[]
             self.arr.append(["""create table if not exists jobs(
             id integer primary key autoincrement,
             user_id integer,
             university text,
             city text,
             job text,
             begin date,
             end date

             );""",[]])
             #self.con.commit()
             #self.con.close()
        def createmany(self,myid,mylist):
            for x in mylist:
                x["user_id"] = myid
                self.arr.append(["insert into jobs (user_id, university, city, job, begin, end) values (:user_id, :university, :city, :job, :begin, :end)",x])
                #self.con.commit()
            #self.con.close()
            return self.arr
        def updatemany(self,myid,mylist):
            ids=[myid]
            myvars=[]
            for x in mylist:
                x["user_id"] = myid
                try:

                  ids.append(x["id"])
                  self.arr.append(["update jobs set user_id = :user_id, university = :university, city = :city, begin = :begin, end = :end where id = :id",x])
                  #self.con.commit()
                  myvars.append("?")
                except:

                  self.arr.append(["insert into jobs (user_id, university, city, job, begin, end) values (:user_id, :university, :city, :job, :begin, :end)",x])

            if len(mylist) > 0:
                self.arr.insert(0,["delete from jobs where user_id = ? and id not in ("+"".join(myvars)+")", ids])
                #self.con.commit()
            else:
                self.arr.insert(0,["delete from jobs where user_id = ?",ids])
                #self.con.commit()
            return self.arr
            #self.con.close()
