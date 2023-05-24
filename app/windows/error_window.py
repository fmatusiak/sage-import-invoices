class ErrorWindow:
    def __init__(self, app):
        self.__app = app

    def getWindowError(self):
        return self.__app.window(title='Sage 100')

    def exists(self):
        try:
            self.__app.window(title='Sage 100').wait('visible', 2)
            return True
        except Exception:
            return False
