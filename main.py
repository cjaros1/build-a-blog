import os
import webapp2
import jinja2
import random
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class NewPost(Handler):
    def render_newpost(self, error=""):
        self.render("newpost.html",  error = error)
    def get(self):
        self.render_newpost()
    def post(self):
        logged_in=False
        title = self.request.get("title")
        entry = self.request.get("entry")

        author="anon"
        if not logged_in:
            author="anon"
        else:
            author=username
        if title and entry:
            b = BlogsDB(title = title, entry = entry,  author=author)
            b.put()
            self.redirect("/blog")
        else:
            error = "we need both a title and blog entry!"
            self.render_newpost(error)


class Blog(Handler):
    def render_blog(self):
        entries = db.GqlQuery("SELECT  * FROM BlogsDB ORDER BY created DESC LIMIT 5")
        self.render("blog.html",entries=entries)
    def get(self):
        self.render_blog()

class Index(Handler):
    def get(self):
        self.redirect('/newpost')

class AllBlogs(Handler):
    def render_all_blogs(self):
        entries=db.GqlQuery("SELECT * FROM BlogsDB ORDER BY created DESC")
        self.render("allblogs.html",entries=entries)
    def get(self):
        self.render_all_blogs()

class ViewPostHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_view_post(self,id):
        entry=BlogsDB.get_by_id(int(id))
        self.render("viewpost.html",entry=entry)
    def get(self, id):
        self.render_view_post(id)
    def post(self):
        id=self.request.get("id")


class BlogsDB(db.Model):
    title = db.StringProperty(required = True)
    entry = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    author=db.StringProperty(required=True)



app = webapp2.WSGIApplication([('/', Index),
                               ('/blog', Blog),
                               ('/newpost', NewPost),
                               ('/allblogs', AllBlogs),
                               webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
                               ], debug=True)
