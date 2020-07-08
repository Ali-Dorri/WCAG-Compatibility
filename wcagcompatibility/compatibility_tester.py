from selenium import webdriver


class CompatibilityTester:

    def __init__(self, browser):
        if browser is not None:
            self.browser = browser
        else:
            self.browser = webdriver.Firefox()

    def open_url(self, url):
        self.browser.get(url)

    def test_table_header(self):
        """Return true if all tables has header, false otherwise"""
        pass

    def test_html_language(self):
        """Returns true if html has language attribute, false otherwise"""
        pass

    def test_page_title(self):
        """Returns true if all pages have head and title attributes, false otherwise"""
        print('called test_page_title')
        pass

    def test_html_deprecated(self):
        """Returns true if no deprecated html 5 attributes is used, false otherwise"""
        pass

    def test_image_rect(self):
        """Returns true if all images has width and height attribute, false otherwise"""
        pass

    def test_table_description(self):
        """Returns true if all tables have description, false otherwise"""
        pass

    def test_labeled_input_select_textarea(self):
        """Returns true if all input, select and textarea elements have label, false otherwise"""
        pass

    def test_identical_link_targets(self):
        """Returns true if all links with identical text have identical targets, false otherwise"""
        pass
