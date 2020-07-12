from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from wcagcompatibility.table_header_checker import TableHeaderChecker
from wcagcompatibility.utility import Utility


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
        images = self.browser.find_elements_by_tag_name('img')
        if images:
            for image in images:
                width = image.get_attribute('width')
                height = image.get_attribute('height')
                if not width and height:
                    message = Utility.get_message(image)
                    message = Utility.add_message(message, 'there is no width and height attributes')
                    return False, message
                elif not width:
                    message = Utility.get_message(image)
                    message = Utility.add_message(message, 'there is no width attribute')
                    return False, message
                elif not height:
                    message = Utility.get_message(image)
                    message = Utility.add_message(message, 'there is no height attribute')
                    return False, message
                else:
                    return True, None
        else:
            return True, None

    def test_table_description(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all tables have description, false otherwise"""
        tables = self.browser.find_elements_by_tag_name('table')
        if tables:
            compliant = True
            messages = []
            for table in tables:
                compliant_message = self.check_table_description(table)
                compliant = compliant & compliant_message[0]
                if not compliant:
                    messages.append(compliant_message[1])
            return compliant, messages
        else:
            return True, ['page has no table']

    def test_labeled_input_select_textarea(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all input, select and textarea elements have label, false otherwise"""
        pass

    def test_identical_link_targets(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all links with identical text have identical targets, false otherwise"""
        pass

    def check_table_description(self, table):
        role = table.get_attribute('role')
        if role is not None and (role == 'presentation' or role == 'none'):
            return True, 'table role attribute is ' + role
        else:
            aria_hidden = table.get_attribute('aria-hidden')
            if aria_hidden:
                return True, 'table aria-hidden attribute is true'

        try:
            caption = table.find_element_by_tag_name('caption')
            if caption and caption.text:
                return True, 'table has caption'

            describe_id = table.get_attribute('aria-describedby')
            if describe_id:
                describer = self.browser.find_element_by_id(describe_id)
                if describer and describer.text:
                    return True, 'table has aria-describedby reference to ' + describe_id

            summary = table.get_attribute('summary')
            if summary:
                return True, 'table has summary attribute'

            figure = table.find_element_by_xpath('..')
            if figure:
                figure_caption = figure.find_element_by_tag_name('figurecaption')
                if figure_caption and figure_caption.text:
                    return True, 'table is in figure tag which has figurecaption tag in it'
        except NoSuchElementException:
            pass

        message = Utility.get_message(table)
        message = Utility.address_message(message, 'table has no description')
        return False, message





