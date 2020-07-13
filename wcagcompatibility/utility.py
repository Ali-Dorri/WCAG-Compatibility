from selenium import webdriver


class Utility:

    @staticmethod
    def get_message(web_element):
        tag_name = web_element.tag_name
        name = web_element.get_attribute('name')
        element_id = web_element.get_attribute('id')
        value = web_element.get_property('value')
        class_attribute = web_element.get_attribute('class')
        text = web_element.get_attribute('textContent')
        message = 'in {0} with {1}=={2}'
        if element_id:
            return message.format(tag_name, 'id', element_id)
        elif name:
            return message.format(tag_name, 'name', name)
        elif value:
            return message.format(tag_name, 'value', value)
        elif class_attribute:
            return message.format(tag_name, 'class', class_attribute)
        elif text:
            return message.format(tag_name, 'text', text)
        else:
            return 'in ' + tag_name

    @staticmethod
    def add_message(message_left, message_right):
        return message_left + ', ' + message_right

    @staticmethod
    def address_message(address, message):
        return address + ': ' + message
