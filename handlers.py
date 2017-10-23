class Handler():
    def can_handle(self, message):
        raise NotImplementedError('Implement this method')

    def handle(self, message, display):
        raise NotImplementedError('Implement this method')


class TagHandler(Handler):
    def get_tag(self):
        raise NotImplementedError('Implement this method')

    def can_handle(self, message):
        return 'text' in message and self.get_tag() in message['text']

    def get_filtered_text(self, message):
        text = message['text']

        # TODO Only remove tag when either side of the message, and not part of the messgae
        return text.replace(self.get_tag(), '').strip()


class TextTagHandler(TagHandler):
    def __init__(self):
        pass

    def get_tag(self):
        return '#text'

    def handle(self, message, display):
        text = self.get_filtered_text(message)
        display.draw_text(text)

# class PictureHandler(Handler):
#     def __init__(self):
#         pass
#
#     name = 'Picture Handler'
#
#     def can_handle(self, message):
#         is_image = False
#         if 'file' in message:
#             message_file = message['file']
#             file_type = message_file['filetype']
#
#             is_image = file_type is 'jpg'
#
#          return is_image
#
#
#     def handle(self, message, display):
#         #if 'file' in message:
#             #message_file = message['file']
#             #file_url = message_file['']
#         pass
