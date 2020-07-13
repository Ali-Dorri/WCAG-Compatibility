from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from wcagcompatibility.html_deprecated_checker import HtmlDeprecatedChecker
from wcagcompatibility.table_header_checker import TableHeaderChecker
from wcagcompatibility.utility import Utility


class CompatibilityTester:

    def __init__(self, browser):
        self.html_deprecated_checker = HtmlDeprecatedChecker()
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
                return False, ['head tag has no title tag']
        else:
            return False, ['page has no head tag']

    def test_html_deprecated(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if no deprecated html 5 attributes is used, false otherwise"""
        return self.html_deprecated_checker.check_rule(self.browser)

    def test_image_rect(self):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all images has width and height attribute, false otherwise"""
        images = self.browser.find_elements_by_tag_name('img')
        if images:
            compliant = True
            messages = []
            for image in images:
                width = image.get_attribute('width')
                height = image.get_attribute('height')
                message = Utility.get_message(image)
                if not width and not height:
                    message = Utility.add_message(message, 'there is no width and height attributes')
                    messages.append(message)
                    compliant = compliant and False
                elif not width:
                    message = Utility.add_message(message, 'there is no width attribute')
                    messages.append(message)
                    compliant = compliant and False
                elif not height:
                    message = Utility.add_message(message, 'there is no height attribute')
                    messages.append(message)
                    compliant = compliant and False
                else:
                    compliant = compliant and True
            return compliant, messages
        else:
            return True, ['page has no image']

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
        a_tags = self.browser.find_elements_by_tag_name('a')
        if a_tags:
            messages = []
            compliant = True
            index_outer = 0
            searched_links_count = 0;
            while index_outer < len(a_tags) and index_outer < 100:
                a_left = a_tags[index_outer]
                index_inner = index_outer + 1
                while index_inner < len(a_tags) and index_inner < 100:
                    a_right = a_tags[index_inner]
                    text_left = a_left.text
                    text_right = a_right.text
                    if a_left != a_right and text_left and text_right and text_left == text_right:
                        url_left = a_left.get_attribute('href')
                        url_right = a_right.get_attribute('href')
                        is_equal_links = self.is_links_equal(url_left, url_right)
                        if not is_equal_links:
                            message = 'link with text=={0}, target=={1}'
                            message_left = message.format(text_left, url_left)
                            message_right = message.format(text_right, url_right)
                            message = Utility.add_message(message_left, message_right)
                            messages.append(message)
                            compliant = compliant and False
                        else:
                            compliant = compliant and True
                    index_inner += 1
                    searched_links_count += 1
                index_outer += 1
            message = 'searched {0} links, at most 10000. I need my CPU!'.format(searched_links_count)
            messages.append(message)
            return compliant, messages
        else:
            return True, 'there is no link'

    def check_table_description(self, table):
        message = Utility.get_message(table)
        role = table.get_attribute('role')
        if role is not None and (role == 'presentation' or role == 'none'):
            message = Utility.address_message(message, 'table role attribute is ' + role)
            return True, message
        else:
            aria_hidden = table.get_attribute('aria-hidden')
            if aria_hidden:
                message = Utility.address_message(message, 'table aria-hidden attribute is true')
                return True, message

        try:
            caption = table.find_element_by_tag_name('caption')
            if caption and caption.text:
                message = Utility.address_message(message, 'table has caption')
                return True, message

            describe_id = table.get_attribute('aria-describedby')
            if describe_id:
                describer = self.browser.find_element_by_id(describe_id)
                if describer and describer.text:
                    message = Utility.address_message(message, 'table has aria-describedby reference to ' + describe_id)
                    return True, message

            summary = table.get_attribute('summary')
            if summary:
                message = Utility.address_message(message, 'table has summary attribute')
                return True, message

            figure = table.find_element_by_xpath('..')
            if figure:
                figure_caption = figure.find_element_by_tag_name('figurecaption')
                if figure_caption and figure_caption.text:
                    message = Utility.address_message(message, 'table is in figure tag which has figurecaption tag in it')
                    return True, message
        except NoSuchElementException:
            pass

        message = Utility.address_message(message, 'table has no description')
        return False, message

    def is_links_equal(self, url_left, url_right):
        return url_left == url_right





