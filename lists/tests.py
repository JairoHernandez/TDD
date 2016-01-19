
from django.core.urlresolvers import resolve # resolve is the function Django uses internally to resolve URLs amd find which view functions they should map to. We're checking that resolve when called with '/', the root of the site, finds a function called homepage.
from django.test import TestCase
from lists.views import home_page # home_page is the view function
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

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
	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)
		#print(response.content.decode())
		self.assertIn('A new list item', response.content.decode())

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')


