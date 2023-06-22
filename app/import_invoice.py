import math

from app.fill_invoice_entry import FillInvoiceEntry
from app.functions import isNullOrEmpty
from app.windows.invoice_data_entry_window import InvoiceDataEntryWindow
from app.windows.invoice_list_window import InvoiceListWindow
from app.windows.vendor_list_window import VendorListWindow


class ImportInvoice:
    def __init__(self, app):
        self.__app = app
        self.__invoiceDataEntryWindow = InvoiceDataEntryWindow(app)
        self.__fillInvoiceEntry = FillInvoiceEntry(app)

    def __checkVendorExists(self, vendor):
        self.__invoiceDataEntryWindow.openVendorList()

        vendorListWindow = VendorListWindow(self.__app)

        if not vendorListWindow.vendorExists(vendor):
            raise Exception(f'Vendor {vendor} does not exists')

    def __checkInvoiceExists(self, invoiceNumber):
        self.__invoiceDataEntryWindow.openInvoiceList()

        invoiceListWindow = InvoiceListWindow(self.__app)

        if invoiceListWindow.invoiceExists(invoiceNumber):
            raise Exception(f'Invoice {invoiceNumber} exists')

    def __checkTheRequiredInvoiceData(self, invoice):
        errorFieldsList = []

        if isNullOrEmpty(invoice['invoice_number']):
            errorFieldsList.append('Invoice number')

        if isNullOrEmpty(invoice['vendor']):
            errorFieldsList.append('Vendor')

        if isNullOrEmpty(invoice['invoice_date']):
            errorFieldsList.append('Invoice date')

        if isNullOrEmpty(invoice['invoice_due_date']):
            errorFieldsList.append('Invoice due date')

        if isNullOrEmpty(invoice['invoice_amount']):
            errorFieldsList.append('Invoice amount')

        if errorFieldsList:
            errorFieldsList = ','.join(errorFieldsList)
            raise Exception('Required fields are empty: ' + errorFieldsList)

    def __checkTotal(self, invoiceAmount):
        sageAmount = self.__invoiceDataEntryWindow.getSageTotal()

        if not math.isclose(invoiceAmount, sageAmount):
            raise Exception(
                'Total on invoice is different.Sage:' + str(sageAmount) + ' vs Invoice:' + str(invoiceAmount))

    def __save(self):
        self.__invoiceDataEntryWindow.accept()

    def importInvoice(self, invoice):
        self.__checkTheRequiredInvoiceData(invoice)

        self.__checkInvoiceExists(invoice['invoice_number'])
        self.__checkVendorExists(invoice['vendor'])

        self.__fillInvoiceEntry.fill(invoice)

        self.__checkTotal(invoice['invoice_amount'])

        self.__save()
