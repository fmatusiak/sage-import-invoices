import pywinauto

from app.exceptions.not_found_window_exception import NotFoundWindowException


class WindowHandleFinder:

    def getHandleByContainsWindowName(self, name):
        try:
            return pywinauto.findwindows.find_window(best_match=name)
        except Exception as e:
            raise NotFoundWindowException(name, e)

    def getHandleByWindowName(self, name):
        try:
            return pywinauto.findwindows.find_window(title=name)
        except Exception as e:
            raise NotFoundWindowException(name, e)
