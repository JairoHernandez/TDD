#from django.test import LiveServerTestCase # Allows to play with a dummy DB. It cannot find static files.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # Like "runserver", StaticLiveServerTestCase will find static files
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
#import unittest

#class NewVisitorTest(LiveServerTestCase): # "runserver" automatically finds static files, LiveServerTestCase does not
class NewVisitorTest(StaticLiveServerTestCase): # this is why you use StaticLiveServerTestCase instead

    @classmethod
    def setUpClass(cls): # similar method to "setUp", also provide by "unittest", which is used to do test setup of the whole class--that means it only gets executed once, rather than before every test method.
                         # This is hwere LiveServerTestCase/StaticLiveServerTestCase usually starts up its test server.
        for arg in sys.argv:
            if 'liveserver' in arg: # Look for "liveserver" in sys.argv
                cls.server_url = 'http://' + arg.split('=')[1] # If we find it tell test class to skip normal "setUpClass" and just 
                                                               # store away our staging server URL in a variable called "server_url" instead.
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()


    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
     
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.server_url) # Replaces the hardcoded url.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'), 'Enter a to-do item')
    
        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')
        #time.sleep(15)
        # When she hits enter, the page updates, she is taken to a new URL and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        
        #inputbox.send_keys("\n")
        edith_list_url = self.browser.current_url
        print('edith>>', edith_list_url )
        #self.fail('Finish the test!')
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')


        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information 
        ## of Edith's is coming through from  cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He is less
        # interestuing than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        print('francis>>', francis_list_url)
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied they both go back to sleep

        #self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

    def test_layout_and_styling(self):
        # Edit goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She noticecs the input box is nicely centers
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 
        512, delta=5) # Helps us to deal with rounding errors of the arithmetic to be within +/- 5 pixels.

        # She starts a new list and sees the input is nicely centered too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 
        512, delta=5)




