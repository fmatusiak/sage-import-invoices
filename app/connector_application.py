from pywinauto import Application


class ConnectorApplication:

    def connect(self, handleWindow, timeout=5):
        try:
            return Application().connect(handle=handleWindow, timeout=timeout)
        except Exception as e:
            raise Exception('Error connect to Sage application', e)
