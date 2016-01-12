
from django.core.urlresolvers import resolve # resolve is the function Django uses internally to resolve URLs amd find which view functions they should map to. We're checking that resolve when called with '/', the root of the site, finds a function called homepage.
from django.test import TestCase
from lists.views import home_page # home_page is the view function
from django.http import HttpRequest

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
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))
