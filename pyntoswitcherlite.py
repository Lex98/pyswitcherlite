from abc import ABCMeta, abstractmethod
from itertools import cycle
from time import sleep
from ctypes import windll, c_ulong, byref, sizeof, Structure
user32 = windll.user32


class RECT(Structure):
    _fields_ = [
        ("left", c_ulong),
        ("top", c_ulong),
        ("right", c_ulong),
        ("bottom", c_ulong)]


class GUITHREADINFO(Structure):
    _fields_ = [("cbSize", c_ulong),
                ("flags", c_ulong),
                ("hwndActive", c_ulong),
                ("hwndFocus", c_ulong),
                ("hwndCapture", c_ulong),
                ("hwndMenuOwner", c_ulong),
                ("hwndMoveSize", c_ulong),
                ("hwndCaret", c_ulong),
                ("rcCaret", RECT)
                ]


def get_layout():
    guiThreadInfo = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))
    user32.GetGUIThreadInfo(0, byref(guiThreadInfo))
    dwThread = user32.GetWindowThreadProcessId(guiThreadInfo.hwndCaret, 0)
    print(dwThread)
    return user32.GetKeyboardLayout(dwThread)


class Layout(metaclass=ABCMeta):

    @abstractmethod
    def switch_layout(self):
        pass


class RussianLayout(Layout):
    letters_to_switch = ['ё', '\"', '№', ';', ':', '?', 'й',
                         'ц', 'у', 'к', 'е', 'н', 'г', 'ш',
                         'щ', 'з', 'х', 'ъ', 'ф', 'ы', 'в',
                         'а', 'п', 'р', 'о', 'л', 'д', 'ж',
                         'э', 'я', 'ч', 'с', 'м', 'и', 'т',
                         'ь', 'б', 'ю', '.', 'Ё', 'Й', 'Ц',
                         'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ',
                         'З', 'Х', 'Ъ', '/', 'Ф', 'Ы', 'В',
                         'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж',
                         'Э', 'Я', 'Ч', 'С', 'М', 'И', 'Т',
                         'Ь', 'Б', 'Ю', ',']

    @classmethod
    def switch_layout(cls, switch_to, string):
        return string_switcher(string, cls, switch_to)


class EnglishLayout(Layout):
    letters_to_switch = ['`', '@', '#', '$', '^', '&', 'q',
                         'w', 'e', 'r', 't', 'y', 'u', 'i',
                         'o', 'p', '[', ']', 'a', 's', 'd',
                         'f', 'g', 'h', 'j', 'k', 'l', ';',
                         '\'', 'z', 'x', 'c', 'v', 'b', 'n',
                         'm', ',', '.', '/', '~', 'Q', 'W',
                         'E', 'R', 'T', 'Y', 'U', 'I', 'O',
                         'P', '{', '}', '|', 'A', 'S', 'D',
                         'F', 'G', 'H', 'J', 'K', 'L', ':',
                         '\"', 'Z', 'X', 'C', 'V', 'B', 'N',
                         'M', '<', '>', '?']

    @classmethod
    def switch_layout(cls, switch_to, string):
        return string_switcher(string, cls, switch_to)


class StringToSwitch(object):
    # __slots__ = ('switch_from_russian', 'switch_from_english',
    #              'switching_to_dict', 'layout_dict' 'layout',
    #              'switch_to', 'string')
    switch_from_russian = cycle((EnglishLayout(), RussianLayout()))
    switch_from_english = cycle((RussianLayout(), EnglishLayout()))
    switching_to_dict = {'russian': switch_from_russian,
                         'english': switch_from_english}
    layout_dict = {'russian': RussianLayout(), 'english': EnglishLayout()}

    def __init__(self, string, layout):
        self.layout = layout
        self.switch_to = next(self.switching_to_dict[self.layout])
        self.string = string

    def change_layout(self):
        return self.layout_dict[self.layout].switch_layout(self.switch_to,
                                                           self.string)

    def next_layout(self):
        self.switch_to = next(self.switching_to_dict[self.layout])
        return self.change_layout()


def string_switcher(string, switch_from, switch_to):
    if isinstance(switch_to, switch_from):
        return string

    switch_dict = dict(zip(switch_from.letters_to_switch,
                           switch_to.letters_to_switch))
    string_after_switch = ''

    for letter in string:
        if letter not in switch_dict:
            string_after_switch += letter
        else:
            string_after_switch += switch_dict[letter]

    return string_after_switch


def main():
    bvf = StringToSwitch('dgdsfgdg', 'russian')
    print(bvf.switch_to)


if __name__ == '__main__':
    main()
