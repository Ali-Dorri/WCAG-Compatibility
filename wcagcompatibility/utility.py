from selenium import webdriver


class Utility:

    @staticmethod
    def get_message(web_element):
        tag_name = web_element.tag_name
        name = web_element.get_attribute('name')
        id = web_element.get_attribute('id')
        value = web_element.get_property('value')
        message = 'in {0} with {0}=={1}'
        if id:
            return message.format(tag_name, 'id', id)
        elif name:
            return message.format(tag_name, 'name', name)
        elif value:
            return message.format(tag_name, 'value', value)
        else:
            return 'in ' + tag_name

    @staticmethod
    def add_message(message_left, message_right):
        return message_left + ', ' + message_right

    @staticmethod
    def address_message(address, message):
        return address + ': ' + message
