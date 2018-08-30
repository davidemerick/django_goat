from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrievew_it_later(self):
        # Edith has heard about a cool new online to-do app
        # She goes to check out the home page
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # She is able to enter a to-do item

        # She types "Brainstorm/Setup backlog initial creation session" into a text box

        # When She hits enter, the page updates, and now the page lists

        # "1: Brainstorm backlog" as an item in a to-do list

        # There is still a text box where she is able to add another item

        # She enters "Schedule backlog creation session"

        # The page updates and now shows both items on her list

        # Edith wonders whether the site will remember her list
        # She sees that the site has generated a unique URL for her
        # There is some explanatory text to that effect.

        # She visits the provided URL - her to-do list is still there.

        # Edith is satisfied and moves on with her morning.

if __name__ == '__main__':
    unittest.main(warnings='ignore')