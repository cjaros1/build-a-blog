import os
import webapp2
import jinja2
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


class MainPage(Handler):
    def render_front(self, title="", entry="", error=""):
        entries = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render("front.html", title=title, entry=entry, error = error, entries = entries)
    def get(self):
        self.render_front()
    def post(self):
        title = self.request.get("title")
        entry = self.request.get("entry")
        if title and entry:
            b = Blog(title = title, entry = entry)
            b.put()
            self.redirect("/")
        else:
            error = "we need both a title and blog entry!"
            self.render_front(title, entry, error)


class Blog(db.Model):
    title = db.StringProperty(required = True)
    entry = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)



app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
