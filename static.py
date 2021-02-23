from datetime import datetime


class Static:

    @staticmethod
    def now(): return str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))

    @staticmethod
    def remove_strange_chars(s): return "".join(i for i in s if ord(i) < 128)
