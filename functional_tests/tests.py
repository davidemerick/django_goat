from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

import time

class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # Helper method to wait for row
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app
        # She goes to check out the home page
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #self.fail('Finish the test!')

        # She is able to enter a to-do item

        inputbox = self.browser.find_element_by_id('id_new_item')
        
        self.assertEqual(inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        # She types "Brainstorm/Setup backlog initial creation session" into a text box
        inputbox.send_keys('Brainstorm/Setup initial backlog creation session')
        # When She hits enter, the page updates, and now the page lists
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # "1: Brainstorm backlog" as an item in a to-do list
        self.wait_for_row_in_list_table('1: Brainstorm/Setup initial backlog creation session')

        # There is still a text box where she is able to add another item
        # She enters "Schedule backlog creation session"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Schedule backlog creation session')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates and now shows both items on her list
        self.wait_for_row_in_list_table('1: Brainstorm/Setup initial backlog creation session')
        self.wait_for_row_in_list_table('2: Schedule backlog creation session')
        
        # Edith is satisfied and moves on with her morning.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Brainstorm/Setup initial backlog creation session')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Brainstorm/Setup initial backlog creation session')

        #She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        ## A new user, Francis, visits the site
        ## We use a new browser session to make sure that no information of Edith's comes through
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Brainstorm/Setup initial backlog creation session', page_text)
        self.assertNotIn('Schedule backlog creation', page_text)

        # Francis starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy eggs')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy eggs')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_lists_url, edith_list_url)

        # There is still no trace of Edith's list and Francis list is displayed
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Brainstorm/Setup initial backlog creation session', page_text)
        self.assertIn('Buy eggs', page_text)

        # Satisfied, Francis leaves


