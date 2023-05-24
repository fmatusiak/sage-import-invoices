import time

from pywinauto.keyboard import send_keys


class BaseWindow:

    def tab(self, quantity=1):
        for x in range(quantity):
            send_keys('{TAB}')
            time.sleep(1)

    def send(self, value, with_spaces=False):
        send_keys(value, with_spaces=with_spaces)
        time.sleep(0.5)
        send_keys('{ENTER}')
        time.sleep(1)

    def enter(self, quantity=1):
        for x in range(quantity):
            send_keys('{ENTER}')
            time.sleep(1)
