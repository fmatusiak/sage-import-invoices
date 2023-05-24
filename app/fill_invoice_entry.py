from app.functions import isNullOrEmpty
from app.windows.adjust_window import AdjustWindow
from app.windows.base_window import BaseWindow
from app.windows.error_window import ErrorWindow
from app.windows.invoice_data_entry_window import InvoiceDataEntryWindow


class FillInvoiceEntry(BaseWindow):
    def __init__(self, app):
        self.__invoiceDataEntryWindow = InvoiceDataEntryWindow(app)
        self.__adjustWindow = AdjustWindow(app)
        self.__errorWindow = ErrorWindow(app)

    def __fillHeaders(self, invoice):
        self.__invoiceDataEntryWindow.typeVendor(invoice['vendor'])
        self.__invoiceDataEntryWindow.typeInvoiceNumber(invoice['invoice_number'])

        self.__checkInvoiceAdjust()

        self.__invoiceDataEntryWindow.typeInvoiceDate(invoice['invoice_date'])
        self.__invoiceDataEntryWindow.typeInvoiceAmount(invoice['invoice_amount'])
        self.__invoiceDataEntryWindow.typeInvoiceDueDate(invoice['invoice_due_date'])

    def __checkInvoiceAdjust(self):
        if self.__adjustWindow.exists():
            self.__adjustWindow.skip()

            raise Exception('The invoice is to adjust. Skipping')

    def __fillLines(self, invoice):
        countAddedLines = 1

        for line in invoice['lines']:
            self.__fillLine(line)

            if countAddedLines < len(invoice['lines']):
                self.__invoiceDataEntryWindow.clearLinersRow()

            countAddedLines += 1

    def __fillLine(self, line):
        if not isNullOrEmpty(str(line['job_number'])) and not isNullOrEmpty(
                str(line['cost_code'])) and not isNullOrEmpty(str(line['type'])):

            self.send(str(line['job_number']))

            self.__checkError('job number', str(line['job_number']))

            self.send(str(line['cost_code']))

            self.__checkError('cost code', str(line['cost_code']))

            self.send(str(line['type'][0]))

            self.__checkError('type', str(line['type']))
        else:
            self.tab()

        if isNullOrEmpty(str(line['amount'])):
            raise Exception('Invalid line data in liners . Amount is empty!')

        if isNullOrEmpty(str(line['comment'])):
            raise Exception('Invalid line data in liners . Comment is empty!')

        self.send(str(line['amount']))

        self.__checkError('amount', str(line['type']))

        self.send(str(line['comment']).replace('#', ""), True)

        if self.__glRequired():
            if isNullOrEmpty(str(line['gl'])):
                raise Exception('GL required. GL is empty !!')

            self.send(str(line['gl']))

            self.__checkError('gl', str(line['gl']))

    def __checkError(self, field, value):
        if self.__errorWindow.exists():
            self.enter()

            raise Exception(f'An error occurred after entering the field "{field}" with value "{value}"')

    def __glRequired(self):
        if self.__errorWindow.exists():
            self.enter()
            return True
        return False

    def fill(self, invoice):
        self.__fillHeaders(invoice)

        self.__invoiceDataEntryWindow.liners()

        self.__fillLines(invoice)
