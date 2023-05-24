from app.exceptions.not_found_window_exception import NotFoundWindowException
from app.windows.base_window import BaseWindow


class InvoiceListWindow(BaseWindow):
    __windowName = 'Invoice List'

    def __init__(self, app):
        self.__app = app
        self.__window = self.__getInvoiceListWindow()

    def __getInvoiceListWindow(self):
        try:
            self.__app.window(title=self.__windowName).wait('visible', 10)
            return self.__app.window(title="Invoice List")
        except Exception as e:
            raise NotFoundWindowException(self.__windowName, e)

    def typeInvoiceNumber(self, invoiceNumber):
        self.__window['Edit'].set_focus()
        self.__window['Edit'].set_text(invoiceNumber)
        self.enter()

    def filters(self, invoiceNumber):
        self.typeInvoiceNumber(invoiceNumber)

    def __getInvoicesSearchResult(self):
        self.__window['SysListView32'].wait('visible', 10)
        return self.__window['SysListView32'].texts()

    def invoiceExists(self, invoiceNumber):
        try:
            self.filters(invoiceNumber)

            invoicesResult = self.__getInvoicesSearchResult()

            self.cancel()

            for invoiceResult in invoicesResult:
                if invoiceNumber in invoiceResult:
                    return True
            return False

        except Exception as e:
            self.cancel()
            raise Exception('An error occurred while checking if the invoice exists', e)

    def cancel(self):
        def isEnabled():
            try:
                self.__window['&Cancel'].wait('enabled', 2)
                return True
            except Exception:
                return False

        if not isEnabled():
            return

        self.__window['&Cancel'].wait('visible', 10)
        self.__window['&Cancel'].click()
