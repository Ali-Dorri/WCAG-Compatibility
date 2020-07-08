

class CommandProcessor:

    BROWSER_NOT_CREATED_ERROR = 'browser is not created yet'

    def __init__(self):
        self.browser = None

    def process_command(self, command):
        """Call corresponding function according to command"""

    def create_webdriver(self, driver_name):
        """Create corresponding webdriver and set it to browser"""

    def set_url(self, url):
        if self.browser is not None:
            self.browser.open_url(url)
            print('browser url set')
        else:
            print(self.BROWSER_NOT_CREATED_ERROR)

    def test_table_headers(self):
        """Print if test_table_headers is verified or not"""
        pass

    def test_html_language(self):
        """Print if test_html_language is verified or not"""
        pass

    def test_pages_title(self):
        """Print if test_pages_title is verified or not"""
        pass

    def test_html_deprecateds(self):
        """Print if test_html_deprecateds is verified or not"""
        pass

    def test_image_width_height(self):
        """Print if test_image_width_height is verified or not"""
        pass

    def test_table_description(self):
        """Print if test_table_description is verified or not"""
        pass

    def test_labeled_input_select_textarea(self):
        """Print if test_labeled_input_select_textarea is verified or not"""
        pass

    def test_identical_links_targets(self):
        """Print if test_identical_links_targets is verified or not"""
        pass
