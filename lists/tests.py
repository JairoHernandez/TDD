
from django.core.urlresolvers import resolve # resolve is the function Django uses internally to resolve URLs amd find which view functions they should map to. We're checking that resolve when called with '/', the root of the site, finds a function called homepage.
from django.test import TestCase
from lists.views import home_page # home_page is the view function
from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.
# Silly test
#class SmokeTest(TestCase):

#	def test_bad_math(self):
#		self.assertEqual(1 + 1, 3)

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		#print(response.content)
		expected_html = render_to_string('home.html') # render allows substitution of python variables into HTML
		self.assertEqual(response.content.decode(), expected_html) # decode() converts response.content.bytes into unicode string, which allows us to compare strings with strings, and not bytes with bytes, in other words this avoids testing constants
		#self.assertTrue(response.content.startswith(b'<html>')) # The following 3 are testing constants.
		#self.assertIn(b'<title>To-Do lists</title>', response.content)
		#self.assertTrue(response.content.strip().endswith(b'</html>'))
