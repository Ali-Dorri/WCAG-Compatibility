from selenium import webdriver
from wcagcompatibility.rule_checker import RuleChecker
from wcagcompatibility.utility import Utility


class TableHeaderChecker(RuleChecker):

    def __init__(self):
        self.table_width = 0
        self.headers_width = 0

    def check_rule(self, browser):
        """Returns a tuple consists of compliant status (boolean) and tuple/array of messages (string) for non compliant status.
         Compliant status is true if all tables has header, false otherwise"""
        tables = browser.find_elements_by_tag_name('table')
        if tables:
            compliant = True
            messages = []
            for table in tables:
                compliant_message = self.check_table_header(table)
                compliant = compliant & compliant_message[0]
                if not compliant:
                    messages.append(compliant_message[1])
            return compliant, messages
        else:
            return True, None

    def check_table_header(self, table):
        role = table.get_attribute('role')
        if role is not None and (role == 'presentation' or role == 'none'):
            return True, None
        else:
            aria_hidden = table.get_attribute('aria-hidden')
            if aria_hidden:
                return True, None

        #none of tables's role or aria-hidden attributes are compliant
        compliant_messages = self.check_both_scope_headers_ids(table)
        if not compliant_messages[0]:
            return compliant_messages
        else:
            compliant_messages = self.check_scopes(table)
            if compliant_messages[0]:
                return compliant_messages
            else:
                return self.check_headers_ids(table)

    def check_scopes(self, table):
        rows = table.find_element_by_xpath('/child::tr')
        
        pass

    def check_th_scope(self, cell):
        scope = cell.get_attribute('scope')
        colspan = cell.get_attribute('colspan')
        rowspan = cell.get_attribute('rowspan')
        message = Utility.get_message(cell)
        if scope:
            if scope == 'col' or scope == 'row':
                if colspan:
                    message = Utility.add_message(message, self.get_scope_message(scope, 'colspan', colspan))
                    return False, message
                elif rowspan:
                    message = Utility.add_message(message, self.get_scope_message(scope, 'rowspan', rowspan))
                    return False, message
            elif scope == 'colgroup':
                if rowspan:
                    message = Utility.add_message(message, self.get_scope_message(scope, 'rowspan', rowspan))
                    return False, message
            elif scope == 'rowgroup':
                if colspan:
                    message = Utility.add_message(message, self.get_scope_message(scope, 'colspan', colspan))
                    return False, message
        return True

    def get_scope_message(self, scope, incompatible_name, incompatible):
        return 'scope=={0} and {1}=={2}'.format(scope, incompatible_name, incompatible)

    def is_valid_cell(self, cell, left_cell, top_cell, cell_pos):
        if left_cell:
            if left_cell.tag_name == 'td':
                return cell.tag_name == 'td', self.get_invalid_cell_message(cell_pos, 'th', 'td', left_cell, top_cell)
            else:   # left_cell.tag_name == 'th'
                if top_cell:
                    if top_cell.tag_name == 'td':
                        return cell.tag_name == 'td', self.get_invalid_cell_message(cell_pos, 'th', 'td', left_cell, top_cell)
                    else:  # top_cell.tag_name == 'th'
                        return cell.tag_name == 'th', self.get_invalid_cell_message(cell_pos, 'td', 'th', left_cell, top_cell)
                else:
                    return True, ''

        elif top_cell:
            if top_cell.tag_name == 'td':
                return cell.tag_name == 'td', self.get_invalid_cell_message(cell_pos, 'th', 'td', left_cell, top_cell)
            else:   # top_cell.tag_name == 'th'
                if self.headers_width < self.table_width:
                    return cell.tag_name == 'th', self.get_invalid_cell_message(cell_pos, 'td', 'th', left_cell, top_cell)
                else:   # self.headers_width == self.table_width
                    return True
        else:   # top_cell == None, left_cell == None, cell == table_top_left_cell
            return cell.tag_name == 'th', self.get_invalid_cell_message(cell_pos, 'td', 'th', left_cell, top_cell)

    @staticmethod
    def get_invalid_cell_message(cell_pos, tag_is, tag_must, left_cell, top_cell):
        base_message = 'cell at [{0}, {1}] is {2}, must be {3}'.format(cell_pos[0], cell_pos[1], tag_is, tag_must)

        if left_cell:
            if top_cell:
                adjacent_message = 'left is {0}, top is {1}'.format(left_cell.tag_name, top_cell.tag_name)
            else:
                adjacent_message = 'left is {0}'.format(left_cell.tag_name)
        elif top_cell:
            adjacent_message = 'top is {0}'.format(top_cell.tag_name)
        else:
            adjacent_message = ''

        return base_message + ', ' + adjacent_message

    @staticmethod
    def get_cell_size(cell):
        colspan = cell.get_attribute('colspan')
        rowspan = cell.get_attribute('rowspan')
        width = 1
        height = 1
        if colspan:
            width = int(colspan)
        if rowspan:
            height = int(rowspan)
        return width, height

    def check_headers_ids(self, table):
        pass

    def check_both_scope_headers_ids(self, table):
        pass
