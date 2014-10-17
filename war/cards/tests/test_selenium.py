from time import sleep
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from cards.models import Player


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        import sys
        sys.path.append("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome")
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def admin_login(self):
        # Create a superuser
        Player.objects.create_superuser('superuser', 'superuser@tests.com', 'mypassword')

        # let's open the admin login page
        self.selenium.get("{}{}".format(self.live_server_url, reverse('admin:index')))

        # let's fill out the form with our superuser's username and password
        self.selenium.find_element_by_name('username').send_keys('superuser')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('mypassword')

        # Submit the form
        password_input.send_keys(Keys.RETURN)

    def test_admin_login(self):

        # Create a superuser
        Player.objects.create_superuser('superuser', 'superuser@tests.com', 'mypassword')

        # let's open the admin login page
        self.selenium.get("{}{}".format(self.live_server_url, reverse('admin:index')))

        # let's fill out the form with our superuser's username and password
        self.selenium.find_element_by_name('username').send_keys('superuser')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('mypassword')

        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # sleep for half a second to let the page load
        sleep(.5)

        # We check to see if 'Site administration' is now on the page, this means we logged in successfully
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

    def test_admin_create_card(self):
        self.admin_login()

        # We can check that our Card model is registered with the admin and we can click on it
        # Get the 2nd one, since the first is the header
        self.selenium.find_elements_by_link_text('Cards')[1].click()

        # Let's click to add a new card
        self.selenium.find_element_by_link_text('Add card').click()
