
from django.core.urlresolvers import resolve # resolve is the function Django uses internally to resolve URLs amd find which view functions they should map to. We're checking that resolve when called with '/', the root of the site, finds a function called homepage.
from django.test import TestCase
from .views import home_page, view_list  # home_page is the view function
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest() # Generate request
        response = home_page(request)
        #print(response.content.decode())
        expected_html = render_to_string('home.html') # render allows substitution of python variables into HTML
        #print(expected_html)
        self.assertEqual(response.content.decode(), expected_html) # decode() converts response.content.bytes into unicode string, which allows us to compare strings with strings, and not bytes with bytes, in other words this avoids testing constants

class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'}) # Look at class ListViewTest to understand client attribute.

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first() # The same as doing 'objects.all[0]'
        self.assertEqual(new_item.text, 'A new list item') # Check the item's text is correct

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List() # Create new list object
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_ # Assigns each item to list_ object
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2) # Check list is properly saved

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase): # Checks URL resolution explicitly, tests view functions by calling them, and check that views render templates all at once.
    
    def test_users_list_template(self): # Check that it's using correct template
        response = self.client.get('/lists/%d/' % (list_.id,)) # If you forget the / test will give this error "AssertionError: No templates used to render the response".
        self.assertTemplateUsed(response, 'list.html') # assertTemplateUsed is one of most useful functions Django test client gives us.
        
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)    
