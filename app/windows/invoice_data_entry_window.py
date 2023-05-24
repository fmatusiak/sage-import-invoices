import locale
import time

from app.exceptions.invalid_fill_invoice_entry_exception import InvalidFillInvoiceEntryException
from app.exceptions.not_found_window_exception import NotFoundWindowException
from app.windows.base_window import BaseWindow
from app.windows.error_window import ErrorWindow


class InvoiceDataEntryWindow(BaseWindow):
    __windowName = 'A/P Invoice Data Entry'

    def __init__(self, app):
        self.__app = app
        self.__window = self.__getInvoiceDataEntryWindow()
        self.__errorWindow = ErrorWindow(app)

    def __getInvoiceDataEntryWindow(self):
        try:
            self.__app.window(title_re=f'{self.__windowName}.*').wait('visible', 10)
            invoiceDataEntryWindow = self.__app.window(title_re='A/P Invoice Data Entry.*')

            return invoiceDataEntryWindow
        except Exception as e:
            raise NotFoundWindowException(self.__windowName, e)

    def openInvoiceList(self):
        try:
            self.__window['Button4'].wait('exists enabled visible ready', 10)
            self.__window['Button4'].click()
        except Exception as e:
            raise Exception('Error open invoice list', e)

    def openVendorList(self):
        try:
            self.__window['Button3'].wait('exists enabled visible ready', 10)
            self.__window['Button3'].click()
        except Exception as e:
            raise Exception('Error open vendor list', e)

    def typeVendor(self, vendor):
        try:
            self.__window['Edit'].wait('exists enabled visible ready', 10)
            self.__window['Edit'].click()
            self.__window['Edit'].set_text(vendor)
            self.enter()
        except Exception as e:
            raise InvalidFillInvoiceEntryException('Vendor', vendor, self.__windowName, e)

    def typeInvoiceNumber(self, invoiceNumber):
        try:
            self.__window['Edit3'].wait('exists enabled visible ready', 10)
            self.__window['Edit3'].click()
            self.__window['Edit3'].set_text(invoiceNumber)
            self.enter()
        except Exception as e:
            raise InvalidFillInvoiceEntryException('Invoice number', invoiceNumber, self.__windowName, e)

    def typeInvoiceDate(self, invoiceDate):
        try:
            self.__window['Edit4'].click()
            self.__window['Edit4'].set_text(invoiceDate)
            self.enter()
        except Exception as e:
            raise InvalidFillInvoiceEntryException('Invoice date', invoiceDate, self.__windowName, e)

    def typeInvoiceAmount(self, invoiceAmount):
        try:
            self.__window['Edit8'].click()
            self.__window['Edit8'].set_text(invoiceAmount)
            self.enter()
        except Exception as e:
            raise InvalidFillInvoiceEntryException('Invoice amount', invoiceAmount, self.__windowName, e)

    def typeInvoiceDueDate(self, invoiceDueDate):
        try:
            self.__window['Edit9'].click()
            self.__window['Edit9'].set_text(invoiceDueDate)
            self.enter()
        except Exception as e:
            raise InvalidFillInvoiceEntryException('Invoice due date', invoiceDueDate, self.__windowName, e)

    def cancel(self):
        def isEnabled():
            try:
                self.__window['&Cancel'].wait('enabled', 2)
                return True
            except Exception:
                return False

        if not isEnabled():
            return

        self.__window['&Cancel'].wait('exists enabled visible ready', 10)
        self.__window['&Cancel'].click()

        cancelWindow = self.__errorWindow.getWindowError()

        cancelWindow['&Yes'].wait('exists enabled visible ready', 10)
        cancelWindow['&Yes'].click()

    def accept(self):
        self.__window['&Accept'].wait('visible', 10)
        self.__window['&Accept'].click()

    def liners(self):
        self.tab(5)

        self.__skipComboBox()

    def __skipComboBox(self):
        try:
            self.__window['ComboBox'].wait('exists enabled visible ready', 1)
            self.tab()
        except Exception:
            pass

        try:
            self.__window['ComboBox2'].wait('exists enabled visible ready', 1)
            self.tab()
        except Exception:
            pass

    def clearLinersRow(self):
        self.__window['&Vendor...Button3'].wait('exists enabled visible ready', 5)
        self.__window['&Vendor...Button3'].click()
        time.sleep(1)

    def getSageTotal(self):
        self.__window['&Vendor...Edit2'].wait('visible', 1)
        sageAmount = str(self.__window['&Vendor...Edit2'].texts()[0]).replace(',', '').strip()

        return self.__parseAmount(float(sageAmount))

    def __parseAmount(self, amount):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        return locale.atof(str(locale.format('%.2f', amount)))
