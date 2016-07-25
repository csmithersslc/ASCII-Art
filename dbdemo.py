import os
import jinja2
import webapp2

from google.appengine.ext import db

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

hidden_html = """
<input type="hidden" name="thingy" value"%s">
"""

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
		
class MainPage(Handler):
	def render_front(self, totle="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM ART ORDER BY DESC")
		self.render("front.html", title=title, art=art, error=error)

	def get(self):
		n = self.request.get("n")
		if n:
			n = int(n)
		self.render("shopping_list.html", n=n)

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Art(title = "title", art = art)
			a.put()
			
		else:
			error= "There needs to be a title and some artwork!"
			self.render_front(title, art, error)


app = webapp2.WSGIApplication([('/', MainPage), 'fizzbuzz', FizzBuzzHandler], debug=True)