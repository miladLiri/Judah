from enum import Enum
import config

#message types: error / notice / success / info

class Messages:

    Buffer = list()

    class Type(Enum):

        SUCCESS = ("SUCCESS", config.SUCCESS_MESSAGE_COLOR)
        ERROR = ("ERROR", config.ERROR_MESSAGE_COLOR)
        INFO = ("INFO", config.INFO_MESSAGE_COLOR)
        NOTICE = ("NOTICE", config.NOTICE_MESSAGE_COLOR)


    class Message:

        def __init__(self, title, text, color):

            self.title = title
            self.text = text
            self.color = color

        def get_string(self):
            return self.title + ": " + self.text

        def get_color(self):
            return self.color


    #add new message
    @staticmethod
    def push(type, text):

        if not isinstance(type, Messages.Type):
            return

        Messages.Buffer.append(Messages.Message(type.value[0], text, type.value[1]))


    #present message
    @staticmethod
    def flush():

        data = list()
        for item in Messages.Buffer:
            data.append(item)

        Messages.Buffer.clear()
        return data