from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')


# Checking that page has the word "Django" in its title
assert 'Django' in browser.title
