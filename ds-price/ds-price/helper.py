from types import SimpleNamespace
from datetime import date, timedelta

# https://stackoverflow.com/questions/16279212/how-to-use-dot-notation-for-dict-in-python

class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)

def dt_tomorrow():
    return date.today() + timedelta(days=1)
