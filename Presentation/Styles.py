from prettytable import PrettyTable
from termcolor import colored
from termcolor import COLORS
from Lib.Time import Time
from Managers.Manager import Manager
import config


class DayStyle:

    @staticmethod
    def table_style(title,items, color):

        if not items:
            return DayStyle.title_style(f"{title} List is Empty!",color,True)

        table = PrettyTable()

        headers = list(items[0].keys())
        headers[0] = colored(title,color)
        table.field_names = headers

        for item in items:
            values = list(item.values())
            values[0] = colored(values[0],color)
            if bool(values[-1]):
                values[-1] = colored(values[-1], color)
            table.add_row(values)
        table.align["title"] = "l"
        table.align["comment"] = "l"
        # table.border = False
        table.header = True
        table.horizontal_char = colored("-", color)
        table.vertical_char = " "
        table.junction_char = colored("-", color)
        table.padding_width = 0

        return table.get_string() + "\n"

    @staticmethod
    def title_style(text, color, border = False):

        table = PrettyTable()
        table.add_row([text])
        table.align= "c"

        border_char = " "
        if border:
            border_char = colored("-", color)

        table.border = True
        table.header = False
        table.horizontal_char = border_char
        table.vertical_char = " "
        table.junction_char = border_char
        table.padding_width = 10

        return table.get_string() + "\n"

    @staticmethod
    def show(data) -> str:

        output = str()
        color = config.DAY_MODE_THEME
        header = "today: " + Time().get() + "\n" + "ToDo Progress: " + colored(data["tdlProgress"], color) + 3*" " + "Optional Progress: " + colored(data["optProgress"], color)

        output += DayStyle.title_style(header, color)
        output += DayStyle.table_style("ToDo", data["tdl"], color)
        output += DayStyle.table_style("Optional", data["opt"], color)

        return output



class NightStyle:

    @staticmethod
    def table_style(title, items, color):

        if not items:
            return NightStyle.title_style(f"{title} List is Empty!", True, color)

        table = PrettyTable()

        headers = list(items[0].keys())
        headers[0] = colored(title, color)
        headers.pop()
        table.field_names = headers

        for item in items:
            values = list(item.values())
            if not Manager.tdl.has(values[1]) and not Manager.opt.has(values[1]):
                values[0] = colored(values[0], color)
            values.pop()
            table.add_row(values)
        table.align["title"] = "l"
        table.align["comment"] = "l"
        # table.border = False
        table.header = True
        table.horizontal_char = colored("-", color)
        table.vertical_char = " "
        table.junction_char = colored("-", color)
        table.padding_width = 0

        return table.get_string() + "\n"

    @staticmethod
    def title_style(text, border=False, color = False):

        table = PrettyTable()
        table.add_row([text])
        table.align = "c"

        border_char = " "
        border_color = "white"
        if border and color:
            border_char = "-"
            border_color = color

        table.border = True
        table.header = False
        table.horizontal_char = colored(border_char, border_color)
        table.vertical_char = " "
        table.junction_char = colored(border_char, border_color)
        table.padding_width = 10

        return table.get_string() + "\n"

    @staticmethod
    def status(data) -> str:

        color = config.NIGHT_MODE_THEME
        output = str()

        output += NightStyle.table_style("ToDo", data["tdl"], color)
        output += NightStyle.table_style("Optional", data["opt"], color)
        output += NightStyle.table_style("All Tasks", data["tasks"], color)

        return output

    @staticmethod
    def confirm_message(text):
        return colored(text, config.CONFIRM_MESSAGE_COLOR)

class MessageStyle:

    @staticmethod
    def show_message(text, color):

        return colored(4*" " + text, color)