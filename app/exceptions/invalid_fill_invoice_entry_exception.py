class InvalidFillInvoiceEntryException(Exception):
    def __init__(self, fieldName, value, windowName, errors):
        self.__fieldName = fieldName
        self.__value = value
        self.__windowName = windowName

        super().__init__(errors)

    def __str__(self):
        return f'There was an error filling "{self.__fieldName}" field with a value "{self.__value}" in "{self.__windowName}" '
