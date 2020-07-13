from selenium.common.exceptions import NoSuchElementException

from wcagcompatibility.rule_checker import RuleChecker
from wcagcompatibility.utility import Utility


class HtmlDeprecatedChecker(RuleChecker):

    # first one in each tuple is an attribute and the rest are tags
    DEPRECATED_ATTRIBUTE_TAGS = [
        ('accept', 'form'),
        ('align', 'caption', 'col', 'div', 'embed', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'iframe', 'img', 'input', 'legend', 'object', 'p', 'table', 'tbody', 'thead', 'tfoot', 'td', 'th', 'tr'),
        ('alink', 'body'),
        ('allowtransparency', 'iframe'),
        ('archive', 'object'),
        ('axis', 'td', 'th'),
        ('background', 'body', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th'),
        ('bgcolor', 'body', 'table', 'td', 'th', 'tr'),
        ('border', 'img', 'object'),
        ('bordercolor', 'table'),
        ('cellpadding', 'table'),
        ('cellspacing', 'table'),
        ('char', 'col', 'tbody', 'thead', 'tfoot', 'td', 'th', 'tr'),
        ('charoff', 'col', 'tbody', 'thead', 'tfoot', 'td', 'th', 'tr'),
        ('charset', 'a', 'link'),
        ('classid', 'object'),
        ('clear', 'br'),
        ('code', 'object'),
        ('codebase', 'object'),
        ('codetype', 'object'),
        ('color', 'hr'),
        ('compact', 'dl', 'ol', 'ul'),
        ('coords', 'a'),
        ('datafld', 'a', 'applet', 'button', 'div', 'fieldset', 'frame', 'iframe', 'img', 'input', 'label', 'legend', 'marquee', 'object', 'param', 'select', 'span', 'textarea'),
        ('dataformatas', 'button', 'div', 'input', 'label', 'legend', 'marquee', 'object', 'option', 'select', 'span', 'table'),
        ('datapagesize', 'table'),
        ('datasrc', 'a', 'applet', 'button', 'div', 'frame', 'iframe', 'img', 'input', 'label', 'legend', 'marquee', 'object', 'option', 'select', 'span', 'table', 'textarea'),
        ('declare', 'object'),
        ('event', 'script'),
        ('for', 'script'),
        ('frame', 'table'),
        ('frameborder', 'iframe'),
        ('height', 'td', 'th'),
        ('hspace', 'embed', 'iframe', 'img', 'input', 'object'),
        ('ismap', 'input'),
        ('langauge', 'script'),
        ('link',  'body'),
        ('lowsrc' ,  'img'),
        ('marginbottom'  ,  'body'),
        ('marginheight' ,   'body', 'iframe'),
        ('marginleft'  ,  'body'),
        ('marginright' ,   'body'),
        ('margintop'  ,  'body'),
        ('marginwidth' ,   'body', 'iframe'),
        ('methods'  ,  'a', 'link'),
        ('name'   , 'a', 'embed', 'img', 'option'),
        ('nohref'  ,  'area'),
        ('noshade' ,   'hr'),
        ('nowrap'  ,  'td', 'th'),
        ('profile' ,   'head'),
        ('rules'   , 'table'),
        ('scheme'  ,  'meta'),
        ('scope'  ,  'td'),
        ('scrolling'  ,  'iframe'),
        ('shape' ,   'a'),
        ('size'  ,  'hr'),
        ('standby'  ,  'object'),
        ('summary' ,   'table'),
        ('target'  ,  'link'),
        ('text'  ,  'body'),
        ('type' ,   'li', 'param', 'ul'),
        ('urn'  ,  'a', 'link'),
        ('usemap'  ,  'input'),
        ('valign'  ,  'col', 'tbody', 'thead', 'tfoot', 'td', 'th', 'tr'),
        ('valuetype' ,   'param'),
        ('version' ,   'html'),
        ('vlink'  ,  'body'),
        ('vspace' ,   'embed', 'iframe', 'img', 'input', 'object'),
        ('width'  ,  'col', 'hr', 'pre', 'table', 'td', 'th')
    ]

    def check_rule(self, browser):
        compliant = True
        messages = []
        for attribute_tag in self.DEPRECATED_ATTRIBUTE_TAGS:
            search_result = self.is_attribute_exists(browser, attribute_tag)
            compliant = compliant and not search_result[0]
            if search_result[0]:
                messages.extend(search_result[1])
        return compliant, messages

    def is_attribute_exists(self, browser, attribute_tags):
        attribute_name = attribute_tags[0]
        xpath = '//{0}[@{1}]'.format(attribute_tags[1], attribute_name)
        if len(attribute_tags) > 2:
            for index in range(2, len(attribute_tags)):
                xpath = '{0} | //{1}[@{2}]'.format(xpath, attribute_tags[index], attribute_name)

        try:
            elements = browser.find_elements_by_xpath(xpath)
            if elements:
                messages = []
                for element in elements:
                    message = Utility.get_message(element)
                    message = Utility.address_message(message, 'has deprecated ' + attribute_name + ' attribute')
                    messages.append(message)
                return True, messages
            else:
                return False, None
        except NoSuchElementException:
            return False, None
