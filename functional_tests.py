from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app
        # She goes to check out the home page
        self.browser.get('http://localhost:8000')

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
        self.check_for_row_in_list_table('1: Brainstorm/Setup initial backlog creation session')

        # There is still a text box where she is able to add another item
        # She enters "Schedule backlog creation session"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Schedule backlog creation session')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates and now shows both items on her list
        self.check_for_row_in_list_table('1: Brainstorm/Setup initial backlog creation session')
        self.check_for_row_in_list_table('2: Schedule backlog creation session')

        # Edith wonders whether the site will remember her list
        # She sees that the site has generated a unique URL for her
        # There is some explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits the provided URL - her to-do list is still there.

        # Edith is satisfied and moves on with her morning.

if __name__ == '__main__':
    unittest.main(warnings='ignore')