from directory import Directory
from render_figure import RenderFigure
from user import User
import re
import traceback
import sys

class Route():
    def __init__(self):
        self.Program=Directory("mon petit guide de python")
        self.Program.set_path("./")
        self.mysession={"notice":None,"email":None,"name":None}
        self.dbUsers=User()
        self.render_figure=RenderFigure(self.Program)
    def set_my_session(self,x):
          print("set session",x)
          self.Program.set_my_session(x)
          self.render_figure.set_session(self.Program.get_session())
    def set_redirect(self,x):

          self.Program.set_redirect(x)
          self.render_figure.set_redirect(self.Program.get_redirect())
    def set_session(self,x):
          print("set session",x)
          self.Program.set_session(x)
          self.render_figure.set_session(self.Program.get_session())
    def logout(self,search):
        self.Program.logout()
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def login(self,search):
        self.user=self.dbUsers.getbyemailpw(search["email"][0],search["password"][0])
        print("user trouve", self.user)
        if self.user["email"]:
          self.set_session(self.user)
          self.set_redirect("/welcome")
        else:
          self.set_redirect("/")
        print("session login",self.Program.get_session())
        return self.render_figure.render_redirect()
    def welcome(self,search):
        return self.render_figure.render_figure("welcome/index.html")
    def delete_user(self,params={}):
        getparams=("id",)
        myparam=dict(zip(getparams,params["routeparams"]))
        self.render_figure.set_param("user",User().deletebyid(myparam["id"]))
        self.set_redirect("/welcome")
        return self.render_figure.render_redirect()
    def edit_user(self,params={}):
        getparams=("id",)
        myparam=dict(zip(getparams,params["routeparams"]))
        self.render_figure.set_param("user",User().getbyid(myparam["id"]))
        return self.render_figure.render_figure("welcome/edituser.html")
    def seeuser(self,params={}):
        getparams=("id",)
        myparam=dict(zip(getparams,params["routeparams"]))
        self.render_figure.set_param("user",User().getbyid(myparam["id"]))
        return self.render_figure.render_figure("welcome/showuser.html")
    def myusers(self,params={}):
        self.render_figure.set_param("users",User().getall())
        return self.render_figure.render_figure("welcome/users.html")
    def update_user(self,params={}):
        getparams=("id",)
        myparam=dict(zip(getparams,params["routeparams"]))
        self.user=self.dbUsers.update(params)
        self.set_session(self.user)
        self.set_redirect(("/seeuser/"+params["id"][0]))
        return self.render_figure.render_redirect()
    def save_user(self,params={}):
        self.user=self.dbUsers.create(params)
        if self.user["email"]:
          self.set_session(self.user)
          self.set_redirect("/welcome")
        else:
          self.set_redirect("/")
          return self.render_figure.render_redirect()
    def data_reach(self,search):
        return self.render_figure.render_figure("welcome/datareach.html")
    def run(self,redirect=False,redirect_path=False,path=False,session=False,params={},url=False):
        if url:
            print("url : ",url)
            self.Program.set_url(url)
        self.set_my_session(session)
        self.render_figure.set_param("current_user_email",self.Program.get_session()["email"])
        self.render_figure.set_param("current_user_name",self.Program.get_session()["name"])
        if redirect:
            self.redirect=redirect
        if redirect_path:
            self.redirect_path=redirect
        if not self.render_figure.partie_de_mes_mots(balise="section",text=self.Program.get_title()):
            self.render_figure.ajouter_a_mes_mots(balise="section",text=self.Program.get_title())
        if path:
            ROUTES={
                    '/logmeout':self.logout,
                    '/save_user':self.save_user,
                    '/update_user':self.update_user,
                    "^/seeuser/([0-9]+)$":self.seeuser,
                    "^/edituser/([0-9]+)$":self.edit_user,
                    "^/deleteuser/([0-9]+)$":self.delete_user,
                    '/data_reach':self.data_reach,
                    '/login':self.login,

                    '/welcome':self.myusers,
                    '/': self.welcome,
                    }
            REDIRECT={"/save_user": "/welcome"}
            patterns=ROUTES.keys()
            functions=ROUTES.values()
            for pattern,case in zip(patterns,functions):
               print("pattern=",pattern)
               x=(re.match(pattern,path))
               if x:
                   params["routeparams"]=x.groups()
                   #if not self.Program.get_redirect():
                   try:
                       self.Program.set_html(html=case(params))
                   except Exception:  
                       self.Program.set_html(html="<p>une erreur s'est produite "+str(traceback.format_exc())+"</p><a href=\"/\">retour à l'accueil</a>")
                   self.Program.redirect_if_not_logged_in()
                   return self.Program
               else:
                   self.Program.set_html(html="<p>la page n'a pas été trouvée</p><a href=\"/\">retour à l'accueil</a>")
            return self.Program
