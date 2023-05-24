class NotFoundWindowException(Exception):
    def __init__(self, windowName, errors):
        self.__windowName = windowName
        super().__init__(errors)

    def __str__(self):
        return f'Window "{self.__windowName}" not found!'
