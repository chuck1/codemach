from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import django.urls

from selenium.webdriver.firefox.webdriver import WebDriver

import core.models

class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_view_sheet(self):
        
        user = core.models.User.objects.create_user('test', 'test@test', 'password')
        user.is_staff = True
        user.save()
        

        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys("test")

        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("password")

        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        WebDriverWait(self.selenium, 10).until(EC.title_is("Site administration | Django site admin"))
        
        #
        if 1:
            self.selenium.get('%s%s' % (self.live_server_url, django.urls.reverse('sheets:index')))
       
            text_input = self.selenium.find_element_by_name("book_name")
            text_input.send_keys("selenium test book")

            self.selenium.find_element_by_xpath('//input[@value="new book"]').click()

