from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException

from wcagcompatibility.compatibility_tester import CompatibilityTester


class CommandProcessor:

    BROWSER_NOT_CREATED_ERROR = 'browser is not created yet!'

    def __init__(self):
        self.compatibility_tester = None

    def process_command(self, command):
        """Call corresponding function according to command"""
        command_args = command.split()
        if command_args.__len__() == 0:
            return None

        print(command_args)
        if command_args[0] == 'create_driver' or command_args[0] == 'create_webdriver':
            if command_args.__len__() > 1:
                self.create_webdriver(command_args[1])
            else:
                print('No input web driver was sent!')
        elif command_args[0] == 'open_url':
            if command_args.__len__() > 1:
                self.open_url(command_args[1])
            else:
                print('No input url was sent!')
        elif command_args[0] == 'test_all':
            self.test_all()
        elif command_args[0] == 'test_table_header':
            self.test_table_header()
        elif command_args[0] == 'test_html_language':
            self.test_html_language()
        elif command_args[0] == 'test_page_title':
            self.test_page_title()
        elif command_args[0] == 'test_html_deprecated':
            self.test_html_deprecated()
        elif command_args[0] == 'test_image_rect':
            self.test_image_rect()
        elif command_args[0] == 'test_table_description':
            self.test_table_description()
        elif command_args[0] == 'test_labeled_input_select_textarea':
            self.test_labeled_input_select_textarea()
        elif command_args[0] == 'test_identical_link_targets':
            self.test_identical_link_targets()
        else:
            print('command is invalid')

    def create_webdriver(self, driver_name):
        """Create corresponding webdriver and set it to compatibility tester"""
        if driver_name == 'chrome':
            self.set_browser(webdriver.Chrome())
        elif driver_name == 'firefox':
            self.set_browser(webdriver.Firefox())
        elif driver_name == 'android':
            self.set_browser(webdriver.Android())
        elif driver_name == 'blackberry':
            self.set_browser(webdriver.BlackBerry())
        elif driver_name == 'edge':
            self.set_browser(webdriver.Edge())
        elif driver_name == 'ie':
            self.set_browser(webdriver.Ie())
        elif driver_name == 'opera':
            self.set_browser(webdriver.Opera())
        elif driver_name == 'phantomjs':
            self.set_browser(webdriver.PhantomJS())
        elif driver_name == 'remote':
            self.set_browser(webdriver.Remote())
        elif driver_name == 'safari':
            self.set_browser(webdriver.Safari())
        elif driver_name == 'webkitgk':
            self.set_browser(webdriver.WebKitGTK())
        else:
            print('web driver name is invalid')

    def set_browser(self, webdriver):
        self.compatibility_tester = CompatibilityTester(webdriver)
        print('web browser was opened')

    def open_url(self, url):
        if self.compatibility_tester is not None:
            try:
                self.compatibility_tester.open_url(url)
                print('url was opened')
            except InvalidArgumentException:
                print('url is invalid')
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_all(self):
        if self.compatibility_tester is not None:
            self.test_table_header()
            self.test_html_language()
            self.test_page_title()
            self.test_html_deprecated()
            self.test_image_rect()
            self.test_table_description()
            self.test_labeled_input_select_textarea()
            self.test_identical_link_targets()
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_table_header(self):
        """Print if test_table_headers is verified or not"""
        if self.compatibility_tester is not None:
            self.test_rule('table header', self.compatibility_tester.test_table_header)
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_html_language(self):
        """Print if test_html_language is verified or not"""
        if self.compatibility_tester is not None:
            self.test_rule('html language', self.compatibility_tester.test_table_header)
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_page_title(self):
        """Print if test_pages_title is verified or not"""
        if self.compatibility_tester is not None:
            self.test_rule('page title', self.compatibility_tester.test_page_title)
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_html_deprecated(self):
        """Print if test_html_deprecated attributes is verified or not"""
        if self.compatibility_tester is not None:
            self.test_rule('html deprecated', self.compatibility_tester.test_html_deprecated)
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_image_rect(self):
        """Print if test_image_width_height is verified or not"""
        if self.compatibility_tester is not None:
            self.test_rule('image rect area', self.compatibility_tester.test_image_rect)
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_table_description(self):
        """Print if test_table_description is verified or not"""
        if self.compatibility_tester is not None:
            self.test_rule('table description', self.compatibility_tester.test_table_description)
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_labeled_input_select_textarea(self):
        """Print if test_labeled_input_select_textarea is verified or not"""
        if self.compatibility_tester is not None:
            self.test_rule('labeled elements', self.compatibility_tester.test_labeled_input_select_textarea)
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_identical_link_targets(self):
        """Print if test_identical_links_targets is verified or not"""
        if self.compatibility_tester is not None:
            self.test_rule('identical links', self.compatibility_tester.test_identical_link_targets)
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    @staticmethod
    def test_rule(rule_name, rule_test):
        print('testing ' + rule_name + '...')
        compliant = rule_test()
        if compliant:
            print(rule_name + ' rule is compliant')
        else:
            print(rule_name + ' rule is non compliant')


if __name__ == "__main__":
    processor = CommandProcessor()
    while True:
        try:
            command = input()
            processor.process_command(command)
        except EOFError:
            print('exited')
            break
