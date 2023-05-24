class AdjustWindow:
    def __init__(self, app):
        self.__app = app

    def getWindowAdjust(self):
        return self.__app.window(title_re='Adjust Invoice.*')

    def exists(self):
        try:
            self.__app.window(title_re='Adjust Invoice.*').wait('visible', 2)
            return True
        except Exception:
            return False

    def skip(self):
        try:
            window = self.getWindowAdjust()

            window['&Ok'].wait('exists enabled visible ready', 5)
            window['&Ok'].click()
        except Exception as e:
            raise Exception("Error skip adjust", e)
