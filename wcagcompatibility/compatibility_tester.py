from selenium import webdriver
from wcagcompatibility.table_header_checker import TableHeaderChecker


class CompatibilityTester:

    def __init__(self, browser):
        if browser is not None:
            self.browser = browser
        else:
            self.browser = webdriver.Firefox()

    def open_url(self, url):
        self.browser.get(url)

    def test_table_header(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all tables has header, false otherwise"""
        return TableHeaderChecker(self.browser).check_rule()

    def test_html_language(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if html has language attribute, false otherwise"""
        html_tag = self.browser.find_element_by_tag_name('html')
        lang_attribute = html_tag.get_attribute('lang')
        return bool(lang_attribute), None

    def test_page_title(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all pages have head and title attributes, false otherwise"""
        head = self.browser.find_element_by_xpath('./html/head')
        if head:
            title = head.find_element_by_xpath('./title')
            if title:
                return True, None
            else:
                return False, 'head tag has no title tag'
        else:
            return False, 'page has no head tag'

    def test_html_deprecated(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if no deprecated html 5 attributes is used, false otherwise"""
        pass

    def test_image_rect(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all images has width and height attribute, false otherwise"""
        pass

    def test_table_description(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all tables have description, false otherwise"""
        pass

    def test_labeled_input_select_textarea(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all input, select and textarea elements have label, false otherwise"""
        pass

    def test_identical_link_targets(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all links with identical text have identical targets, false otherwise"""
        pass





